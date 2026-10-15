import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'my_bot'

    # -----------------------------
    # Robot State Publisher
    # -----------------------------
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ]),
        launch_arguments={
            'use_sim_time': 'true',
            'use_ros2_control': 'true'
        }.items()
    )

    # -----------------------------
    # World file path
    # -----------------------------
    world_path = os.path.join(
        get_package_share_directory(package_name),
        'worlds',
        'obstacles.world'
    )

    # -----------------------------
    # Gazebo parameters
    # -----------------------------
    gazebo_params_file = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'gazebo_params.yaml'
    )

    # -----------------------------
    # Gazebo launch (WITH WORLD)
    # -----------------------------
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ]),
        launch_arguments={
            'world': world_path,
            'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file
        }.items()
    )

    # -----------------------------
    # Spawn robot
    # -----------------------------
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'my_bot'
        ],
        output='screen'
    )

    # Delay spawn slightly (prevents race condition)
    delayed_spawn = TimerAction(
        period=3.0,
        actions=[spawn_entity]
    )

    # -----------------------------
    # Controllers
    # -----------------------------
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # -----------------------------
    # Launch everything
    # -----------------------------
    return LaunchDescription([
        rsp,
        gazebo,
        delayed_spawn,
        diff_drive_spawner,
        joint_broad_spawner
    ])