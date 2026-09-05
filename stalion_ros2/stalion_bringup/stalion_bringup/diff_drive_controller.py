#!/usr/bin/env python3
"""
Differential Drive Controller for Stalion base.

Подписывается на /cmd_vel (после Ethical Veto)
Публикует:
  - /left_wheel_vel
  - /right_wheel_vel
  - /odom (простая одометрия)

Параметры соответствуют URDF:
  wheel_separation = 0.60 m
  wheel_radius     = 0.12 m
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Quaternion, TransformStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from tf2_ros import TransformBroadcaster


class DiffDriveController(Node):
    def __init__(self):
        super().__init__("diff_drive_controller")

        # --- Параметры робота (из URDF) ---
        self.declare_parameter("wheel_separation", 0.60)   # расстояние между колёсами, м
        self.declare_parameter("wheel_radius", 0.12)        # радиус колеса, м
        self.declare_parameter("max_linear", 1.0)           # м/с
        self.declare_parameter("max_angular", 2.0)          # рад/с

        self.wheel_separation = self.get_parameter("wheel_separation").value
        self.wheel_radius = self.get_parameter("wheel_radius").value
        self.max_linear = self.get_parameter("max_linear").value
        self.max_angular = self.get_parameter("max_angular").value

        # --- Состояние одометрии ---
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = self.get_clock().now()

        # --- Подписка / публикация ---
        self.sub_cmd = self.create_subscription(
            Twist, "/cmd_vel", self.cmd_callback, 10
        )

        self.pub_left = self.create_publisher(Float64, "/left_wheel_vel", 10)
        self.pub_right = self.create_publisher(Float64, "/right_wheel_vel", 10)
        self.pub_odom = self.create_publisher(Odometry, "/odom", 10)

        self.tf_broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(0.05, self.update_odometry)  # 20 Hz

        self.current_linear = 0.0
        self.current_angular = 0.0

        self.get_logger().info(
            f"DiffDriveController ready | "
            f"sep={self.wheel_separation}m radius={self.wheel_radius}m"
        )

    def cmd_callback(self, msg: Twist):
        """Приём команды скорости (уже после Ethical Veto)."""
        # Ограничение
        linear = max(-self.max_linear, min(self.max_linear, msg.linear.x))
        angular = max(-self.max_angular, min(self.max_angular, msg.angular.z))

        self.current_linear = linear
        self.current_angular = angular

        # Дифференциальная кинематика:
        # v_left  = (v - ω * L/2) / r
        # v_right = (v + ω * L/2) / r
        half_l = self.wheel_separation / 2.0
        v_left = (linear - angular * half_l) / self.wheel_radius
        v_right = (linear + angular * half_l) / self.wheel_radius

        left_msg = Float64()
        left_msg.data = v_left
        right_msg = Float64()
        right_msg.data = v_right

        self.pub_left.publish(left_msg)
        self.pub_right.publish(right_msg)

    def update_odometry(self):
        """Интегрирование одометрии."""
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        self.last_time = now

        if dt <= 0.0 or dt > 1.0:
            return

        # Простое интегрирование
        delta_x = self.current_linear * math.cos(self.theta) * dt
        delta_y = self.current_linear * math.sin(self.theta) * dt
        delta_theta = self.current_angular * dt

        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))  # normalize

        # Odometry message
        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        q = self.yaw_to_quaternion(self.theta)
        odom.pose.pose.orientation = q

        odom.twist.twist.linear.x = self.current_linear
        odom.twist.twist.angular.z = self.current_angular

        self.pub_odom.publish(odom)

        # TF
        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation = q
        self.tf_broadcaster.sendTransform(t)

    @staticmethod
    def yaw_to_quaternion(yaw: float) -> Quaternion:
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)
        return q


def main(args=None):
    rclpy.init(args=args)
    node = DiffDriveController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
