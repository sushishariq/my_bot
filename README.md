# 🤖 Cute Crawler (my_bot)
> **A ROS 2-powered differential drive robot that sees, thinks, and navigates.**

![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?style=for-the-badge&logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-FF6F00?style=for-the-badge&logo=gazebo&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)

<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDl5bjV5Z3V5Y3V5Y3V5Y3V5Y3V5Y3V5Y3V5Y3V5Y3V5Y3V5/placeholder.gif" width="600" alt="Robot Simulation Demo" />
</div>

## 🔥 What is this?
**Cute Crawler** is a custom-built autonomous mobile robot designed to explore the world of ROS 2 (Robot Operating System). It bridges the gap between simulation and reality, running the exact same control logic on a **Raspberry Pi** as it does in **Gazebo**.

It doesn't just drive—it *perceives*. Equipped with Lidar and Camera fusion, it’s built for SLAM, navigation, and obstacle avoidance.

## 🚀 Features
* **🧠 Full ROS 2 Control:** Uses `ros2_control` with `diff_drive_controller` for smooth, physics-based movement.
* **👀 Lidar Perception:** Obstacle detection and mapping using RPLidar.
* **📸 Visual Intelligence:** Pi Camera integration for object detection and following.
* **🏗️ Digital Twin:** A high-fidelity Gazebo simulation that mirrors the real hardware.
* **🎮 Teleoperation:** Drive it with a keyboard, joystick, or autonomous planner.

## 🛠️ The Stack
| Component | Tech Used |
| :--- | :--- |
| **Middleware** | ROS 2 Humble / Jazzy |
| **Simulation** | Gazebo Classic |
| **Hardware** | Raspberry Pi 4, RPLidar, Pi Cam, DC Motors |
| **Control** | `ros2_control`, `diff_drive_controller` |
| **Build System** | Colcon (CMake/Python) |

## ⚡ Quick Start

### 1. Installation
Clone the repo into your ROS 2 workspace:
```bash
cd ~/dev_ws/src
git clone [https://github.com/sushishariq/my_bot.git](https://github.com/sushishariq/my_bot.git)
```

Install dependencies and build:
```bash
cd ~/dev_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

### 2. Launch Simulation 🌍
Fire up the robot in the obstacle world with full physics and controllers:
```bash
ros2 launch my_bot launch_sim.launch.py world:=./src/my_bot/worlds/obstacles.world
```

### 3. Drive It 🚗
Open a new terminal and take control:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```

## 🗺️ Roadmap
- [x] Basic URDF & Xacro Description
- [x] Gazebo Simulation Integration
- [x] ROS 2 Control (Diff Drive & Joint States)
- [ ] Add IMU for 3D Odometry (Robot Localization)
- [ ] SLAM (Mapping) with `slam_toolbox`
- [ ] Nav2 Autonomous Navigation

## 🤝 Contributing
Got a cool idea? Found a bug? Feel free to open an issue or submit a PR. Let's make this crawler even cuter (and smarter)!

---
<div align="center">
  <b>Built with ❤️ by Shariq</b>
</div>
