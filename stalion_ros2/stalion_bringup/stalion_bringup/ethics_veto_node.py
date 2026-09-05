#!/usr/bin/env python3
"""
ROS2 Ethics Veto Node
Подписывается на /cmd_vel_raw, проверяет через FormalEthicalVeto,
публикует безопасную команду в /cmd_vel.
"""

import json
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

import sys
sys.path.append("/home/workdir/artifacts/stalion_core")
try:
    from ethics_veto import FormalEthicalVeto, VetoResult
except ImportError:
    FormalEthicalVeto = None


class EthicsVetoNode(Node):
    def __init__(self):
        super().__init__("ethics_veto_node")
        self.veto = FormalEthicalVeto() if FormalEthicalVeto else None

        self.sub = self.create_subscription(Twist, "/cmd_vel_raw", self.cmd_callback, 10)
        self.pub_safe = self.create_publisher(Twist, "/cmd_vel", 10)
        self.pub_verdict = self.create_publisher(String, "/ethics/verdict", 10)

        self.get_logger().info("EthicsVetoNode active — filtering /cmd_vel_raw → /cmd_vel")

    def cmd_callback(self, msg: Twist):
        action = {
            "linear": abs(msg.linear.x),
            "angular": abs(msg.angular.z),
            "tags": [],
            "risk_to_humans": 0.0
        }

        # Простая эвристика риска
        if abs(msg.linear.x) > 1.2:
            action["tags"].append("high_speed_near_human")
            action["risk_to_humans"] = 0.4
        if abs(msg.linear.x) > 2.0:
            action["tags"].append("aggressive")
            action["risk_to_humans"] = 0.6

        if self.veto is None:
            # Нет veto — пропускаем как есть (небезопасно, только для теста)
            self.pub_safe.publish(msg)
            return

        decision = self.veto.check(action)

        # Публикуем вердикт
        vmsg = String()
        vmsg.data = json.dumps(decision.to_dict(), ensure_ascii=False)
        self.pub_verdict.publish(vmsg)

        if decision.action_blocked:
            # Полная блокировка — публикуем нулевую скорость
            safe = Twist()
            self.pub_safe.publish(safe)
            self.get_logger().warn(f"BLOCKED: {decision.reason}")
        else:
            # Ограничение скорости
            safe = Twist()
            scale = decision.speed_limit
            safe.linear.x = msg.linear.x * scale
            safe.linear.y = msg.linear.y * scale
            safe.angular.z = msg.angular.z * scale
            self.pub_safe.publish(safe)
            if decision.result.value == "restrict":
                self.get_logger().info(f"RESTRICTED: speed_limit={scale}")


def main(args=None):
    rclpy.init(args=args)
    node = EthicsVetoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
