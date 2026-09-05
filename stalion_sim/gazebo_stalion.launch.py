#!/usr/bin/env python3
"""
Простой launch для Gazebo + Stalion URDF.
Требует: ros2 + gazebo_ros (Humble/Jazzy)
"""

import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Пути (измените под свою установку)
    urdf_file = os.path.join(
        os.path.dirname(__file__), "stalion.urdf"
    )
    world_file = os.path.join(
        os.path.dirname(__file__), "stalion_world.sdf"
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="true"),

        # Gazebo
        ExecuteProcess(
            cmd=["gazebo", "--verbose", world_file, "-s", "libgazebo_ros_factory.so"],
            output="screen"
        ),

        # Robot State Publisher
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": open(urdf_file).read(),
                "use_sim_time": True
            }]
        ),

        # Spawn robot
        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=["-entity", "stalion", "-file", urdf_file, "-x", "0", "-y", "0", "-z", "0.2"],
            output="screen"
        ),
    ])
