# 🤖 Cute Crawler (my_bot)
> **A ROS 2 differential drive robot that sees, maps, and (soon) navigates on its own.**

![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?style=for-the-badge&logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-FF6F00?style=for-the-badge&logo=gazebo&logoColor=white)
![SLAM](https://img.shields.io/badge/SLAM-slam__toolbox-4CAF50?style=for-the-badge)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)

## 🔥 What is this?

**Cute Crawler** is a custom differential drive robot built to learn ROS 2 end to end: URDF/Xacro description → Gazebo simulation → `ros2_control` → lidar SLAM → autonomous navigation. The same description and control stack is meant to run on a Raspberry Pi as it does in simulation.

Right now it drives, senses with a 2D lidar and a camera, and builds maps with `slam_toolbox`. Nav2 runs on top of it from the stock `nav2_bringup` launch files — see [Autonomous Navigation](#-4-autonomous-navigation-nav2--amcl).

## 📦 What's actually in this package

`my_bot` is a pure **ament_cmake** package with no compiled code — it ships description, config, launch and world files only.

```
my_bot/
├── description/          # URDF / Xacro robot model
│   ├── robot.urdf.xacro      # top-level; includes everything below
│   ├── robot_core.xacro      # base_link, base_footprint, chassis, wheels, caster
│   ├── inertial_macros.xacro # box/cylinder/sphere inertia helpers
│   ├── ros2_control.xacro    # gazebo_ros2_control hardware interface
│   ├── gazebo_control.xacro  # fallback libgazebo_ros_diff_drive plugin
│   ├── lidar.xacro           # 360-sample ray sensor
│   ├── camera.xacro          # 640x480 RGB camera
│   └── depth_camera.xacro    # RealSense body — NOT included by robot.urdf.xacro yet
├── launch/
│   ├── rsp.launch.py         # robot_state_publisher only
│   └── launch_sim.launch.py  # rsp + Gazebo + spawn + controller spawners
├── config/
│   ├── my_controllers.yaml               # diff_cont + joint_broad
│   ├── gazebo_params.yaml                # Gazebo publish rate
│   ├── twist_mux.yaml                    # nav/joy priorities (not wired into a launch yet)
│   ├── mapper_params_online_async.yaml   # slam_toolbox parameters
│   └── *.rviz                            # main / view_bot / drive_bot displays
└── worlds/
    ├── obstacles.world       # default sim world (~36 models)
    └── empty.world
```

## 🤖 The robot

| Property | Value |
| :--- | :--- |
| Drive type | Differential, 2 driven wheels + spherical caster |
| Wheel radius | `0.035 m` |
| Wheel separation | `0.1503 m` |
| Chassis | `0.25 × 0.1 × 0.05 m` box, `0.5 kg` |
| Frames | `base_link` → `base_footprint`, `chassis`, `laser_frame`, `camera_link(_optical)` |
| Lidar | 360 samples, ±π, `0.3–12 m`, 10 Hz |
| Camera | 640×480, FOV `1.089 rad`, 10 Hz |
| Controller rate | 30 Hz (`controller_manager`), odom published at 50 Hz |

### Key topics

| Topic | Purpose |
| :--- | :--- |
| `/diff_cont/cmd_vel_unstamped` | **Velocity input** (`use_stamped_vel: false`) |
| `/odom` | Wheel odometry, publishes `odom → base_link` TF |
| `/scan/out` | Lidar — note the `/out` suffix, it comes from the ray sensor plugin |
| `/camera/image_raw` | RGB image stream |
| `/joint_states` | From `joint_broad` |

> ⚠️ **The scan topic is `/scan/out`, not `/scan`.** `slam_toolbox` is already configured for it; anything else (Nav2, RViz, rosbag) needs a remap.

## 🛠️ The Stack

| Component | Tech Used |
| :--- | :--- |
| **Middleware** | ROS 2 Humble |
| **Simulation** | Gazebo Classic (`gazebo_ros`, `gazebo_ros2_control`) |
| **Control** | `ros2_control`, `diff_drive_controller`, `joint_state_broadcaster` |
| **Mapping** | `slam_toolbox` (online async) |
| **Navigation** | Nav2 + AMCL (via `nav2_bringup`) |
| **Hardware target** | Raspberry Pi 4, RPLidar, Pi Cam, DC motors |
| **Build System** | Colcon / ament_cmake |

## ⚡ Quick Start

### Install

```bash
cd ~/dev_ws/src
git clone https://github.com/sushishariq/my_bot.git

cd ~/dev_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

You'll also want the runtime packages:

```bash
sudo apt install ros-humble-slam-toolbox ros-humble-navigation2 \
                 ros-humble-nav2-bringup ros-humble-twist-mux \
                 ros-humble-teleop-twist-keyboard
```

> 💡 `config/`, `description/`, `launch/` and `worlds/` are **installed**, not read from source. Build with `--symlink-install` or re-run `colcon build` after editing any YAML or Xacro.

### 1. Launch the simulation 🌍

```bash
ros2 launch my_bot launch_sim.launch.py
```

This brings up `robot_state_publisher`, Gazebo with `worlds/obstacles.world`, spawns the robot after a 3 s delay, then spawns `diff_cont` and `joint_broad`.

> The world is currently **hardcoded** in `launch_sim.launch.py`. To use `empty.world`, edit `world_path` in the launch file and rebuild.

Just the model, no Gazebo (for RViz inspection):

```bash
ros2 launch my_bot rsp.launch.py use_sim_time:=false use_ros2_control:=true
rviz2 -d src/my_bot/config/view_bot.rviz
```

### 2. Drive it 🚗

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```

### 3. Map the world 🗺️

With the sim running:

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=./src/my_bot/config/mapper_params_online_async.yaml \
  use_sim_time:=true
```

```bash
rviz2 -d src/my_bot/config/main.rviz
```

Drive around, watch the map fill in, then save it — **two different formats, you generally want both**:

```bash
# Portable occupancy grid, for map_server / AMCL
ros2 run nav2_map_server map_saver_cli -f ~/dev_ws/my_map_save

# slam_toolbox pose-graph, for resuming mapping or localization mode
ros2 service call /slam_toolbox/serialize_map \
  slam_toolbox/srv/SerializePoseGraph "{filename: '/home/shariq/dev_ws/my_map_serial'}"
```

The workspace already contains a saved map of `obstacles.world`:

| File | What it is |
| :--- | :--- |
| `my_map_save.pgm` / `.yaml` | 303×316 grid @ `0.05 m/px`, origin `[-7.78, -3.83, 0]` |
| `my_map_serial.data` / `.posegraph` | slam_toolbox serialized pose graph |

**Notable SLAM settings** (`config/mapper_params_online_async.yaml`):

| Param | Value |
| :--- | :--- |
| `mode` | `mapping` — switch to `localization` to relocalize on a saved graph |
| `scan_topic` | `/scan/out` |
| `base_frame` | `base_footprint` |
| `resolution` | `0.05` |
| `max_laser_range` | `20.0` (rastering only; the sensor itself stops at 12 m) |
| `solver_plugin` | `solver_plugins::CeresSolver` |

### 4. Autonomous navigation (Nav2 + AMCL) 🧭

There is **no Nav2 launch file or param file in this package yet** — Nav2 is driven from the stock `nav2_bringup` launch files. Two ways to run it:

**a) Localize against the saved map with AMCL:**

```bash
ros2 launch nav2_bringup bringup_launch.py \
  use_sim_time:=true \
  map:=/home/shariq/dev_ws/my_map_save.yaml \
  --ros-args -r /scan:=/scan/out
```

Then set the initial pose with **2D Pose Estimate** in RViz before sending a goal.

**b) Navigate while mapping** (slam_toolbox already running, skip AMCL):

```bash
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true
```

**Three things Nav2 needs from this robot:**

1. **Scan remap** — Nav2 costmaps subscribe to `/scan`, the robot publishes `/scan/out`.
2. **Velocity remap** — Nav2 publishes `/cmd_vel`, the controller listens on `/diff_cont/cmd_vel_unstamped`. Either remap it, or bring up `twist_mux`:
   ```bash
   ros2 run twist_mux twist_mux \
     --ros-args --params-file ./src/my_bot/config/twist_mux.yaml \
     -r cmd_vel_out:=/diff_cont/cmd_vel_unstamped
   ```
3. **Robot footprint / inflation** — the stock Nav2 params assume a much larger robot. This chassis is `0.25 × 0.1 m`; shrink `robot_radius` to ~`0.15` or the planner will refuse to leave the start pose.

## 🗺️ Roadmap
- [x] URDF & Xacro description
- [x] Gazebo Classic simulation
- [x] ROS 2 Control (diff drive & joint state broadcaster)
- [x] Lidar + camera sensors
- [x] SLAM with `slam_toolbox` (online async) + map saving
- [ ] Commit a `nav2_params.yaml` tuned for this footprint
- [ ] `navigation_launch.py` / `localization_launch.py` in this package
- [ ] Wire `twist_mux` into `launch_sim.launch.py`
- [ ] Add IMU + `robot_localization` EKF for fused odometry
- [ ] Enable `depth_camera.xacro` (currently not included in `robot.urdf.xacro`)
- [ ] Real hardware bringup on the Raspberry Pi

## 🐛 Known quirks

- `launch_sim.launch.py` takes **no arguments** — world, sim time and `use_ros2_control` are all hardcoded.
- `config/twist_mux.yaml` exists but nothing launches `twist_mux`.
- `depth_camera.xacro` is visual-only (no depth sensor plugin) and isn't included in the robot.
- `gazebo_control.xacro` (the `use_ros2_control:=false` path) still carries the old chassis numbers — `wheel_separation 0.35`, `wheel_diameter 0.15` — which don't match the actual robot.
- `package.xml` still has placeholder maintainer, description and license fields, and declares no runtime dependencies, so `rosdep install` pulls nothing.

## 🤝 Contributing
Got a cool idea? Found a bug? Open an issue or a PR.

---
<div align="center">
  <b>Built with ❤️ by Shariq</b>
</div>
