# TurtleBot3 ROS 2 Autonomous Patrol

Autonomous patrol system for a **TurtleBot3 Waffle** using **ROS 2 Jazzy**, **Gazebo Sim**, **SLAM Toolbox**, and **Nav2**.

The robot builds/uses a 2D map, localizes itself using AMCL, navigates through manually verified patrol waypoints, avoids obstacles using Nav2, returns to its home position, and continuously repeats the patrol route.

---

## 🤖 Project Overview

This project demonstrates autonomous mobile robot navigation and continuous patrol behavior in simulation.

### Main capabilities

- TurtleBot3 Waffle simulation
- Gazebo Sim environment
- 2D LiDAR-based mapping
- SLAM using SLAM Toolbox
- Saved occupancy-grid map
- AMCL localization
- Nav2 autonomous navigation
- Manually collected and verified patrol waypoints
- Obstacle avoidance through Nav2
- Continuous patrol loop
- Automatic return to home position
- Patrol status logging to CSV
- Navigation speed configured up to **0.4 m/s**

---

## 🧰 Technologies

| Technology | Version / Configuration |
|---|---|
| Ubuntu | 24.04 LTS |
| ROS 2 | Jazzy |
| Gazebo | Sim 8 |
| Robot | TurtleBot3 Waffle |
| Navigation | Nav2 |
| SLAM | SLAM Toolbox |
| Localization | AMCL |
| Sensor | 2D LiDAR |
| Programming | Python |
| Visualization | RViz2 |

---

## 📁 Project Structure

```text
my_Patrolling_robot/
├── config/
│   ├── nav2_params.yaml
│   └── waffle.yaml
├── launch/
│   └── patrol_launch.py
├── maps/
│   ├── patrol_map.pgm
│   └── patrol_map.yaml
├── my_Patrolling_robot/
│   ├── __init__.py
│   └── patrol_node.py
├── resource/
│   └── my_Patrolling_robot
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── .gitignore
├── package.xml
├── setup.cfg
└── setup.py
