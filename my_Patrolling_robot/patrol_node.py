import csv
import os
from datetime import datetime

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


class PatrolNode(Node):

    def __init__(self):
        super().__init__('patrol_node')

        self.navigator = BasicNavigator()

        self.home = (0.0491, -0.0213)

        self.waypoints = [
            (1.0017, -0.0401),
            (1.9677, 0.9899),
            (2.9879, -0.0273),
            (3.4756, 0.8342),
        ]

        log_dir = os.path.expanduser(
            '~/Desktop/ros2_ws/src/my_Patrolling_robot/logs'
        )
        os.makedirs(log_dir, exist_ok=True)

        self.csv_file = os.path.join(log_dir, 'patrol_log.csv')

        self.get_logger().info(
            f'Patrol log: {self.csv_file}'
        )

    def create_pose(self, x, y):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()

        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0

        pose.pose.orientation.z = 0.0
        pose.pose.orientation.w = 1.0

        return pose

    def log_result(self, waypoint, x, y, status):
        file_exists = os.path.exists(self.csv_file)

        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    'timestamp',
                    'waypoint',
                    'x',
                    'y',
                    'status'
                ])

            writer.writerow([
                datetime.now().isoformat(),
                waypoint,
                x,
                y,
                status
            ])

    def navigate_to(self, name, x, y):
        self.get_logger().info(
            f'Navigating to {name}: x={x:.2f}, y={y:.2f}'
        )

        goal = self.create_pose(x, y)
        self.navigator.goToPose(goal)

        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()

            if feedback is not None:
                distance = feedback.distance_remaining

                self.get_logger().info(
                    f'{name}: {distance:.2f} m remaining'
                )

        result = self.navigator.getResult()

        if result == TaskResult.SUCCEEDED:
            status = 'SUCCEEDED'
            self.get_logger().info(f'{name}: SUCCEEDED')

        elif result == TaskResult.CANCELED:
            status = 'CANCELED'
            self.get_logger().warn(f'{name}: CANCELED')

        else:
            status = 'FAILED'
            self.get_logger().error(f'{name}: FAILED')

        self.log_result(name, x, y, status)

        return result == TaskResult.SUCCEEDED

    def run_patrol(self):
        self.get_logger().info('Setting initial pose...')

        initial_pose = self.create_pose(
            self.home[0],
            self.home[1]
        )

        self.navigator.setInitialPose(initial_pose)

        self.get_logger().info(
            f'Initial pose set to HOME: '
            f'x={self.home[0]:.2f}, y={self.home[1]:.2f}'
        )

        self.get_logger().info('Waiting for Nav2...')

        self.navigator.waitUntilNav2Active()

        self.get_logger().info('Nav2 is active.')

        cycle = 0

        while rclpy.ok():
            cycle += 1

            self.get_logger().info(
                f'========== PATROL CYCLE {cycle} =========='
            )

            for index, (x, y) in enumerate(self.waypoints, start=1):
                name = f'WP{index}'

                success = self.navigate_to(
                    name,
                    x,
                    y
                )

                if not success:
                    self.get_logger().warn(
                        f'{name} failed. Returning HOME.'
                    )
                    break

            self.get_logger().info('Returning HOME...')

            self.navigate_to(
                'HOME',
                self.home[0],
                self.home[1]
            )

            self.get_logger().info(
                f'========== CYCLE {cycle} COMPLETE =========='
            )


def main(args=None):
    rclpy.init(args=args)

    node = PatrolNode()

    try:
        node.run_patrol()
    except KeyboardInterrupt:
        node.get_logger().info('Patrol stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
