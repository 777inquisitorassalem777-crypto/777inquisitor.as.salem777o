from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="stalion_bringup",
            executable="pneuma_node",
            name="pneuma_node",
            output="screen",
        ),
        Node(
            package="stalion_bringup",
            executable="ethics_veto_node",
            name="ethics_veto_node",
            output="screen",
        ),
        Node(
            package="stalion_bringup",
            executable="diff_drive_controller",
            name="diff_drive_controller",
            output="screen",
            parameters=[{
                "wheel_separation": 0.60,
                "wheel_radius": 0.12,
                "max_linear": 1.0,
                "max_angular": 2.0,
            }]
        ),
    ])
