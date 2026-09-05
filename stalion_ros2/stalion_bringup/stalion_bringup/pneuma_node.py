#!/usr/bin/env python3
"""
ROS2 node: публикует состояние Пневмы и этический вердикт.
Топики:
  /pneuma/state          (std_msgs/Float32MultiArray)
  /pneuma/status         (std_msgs/String)  — JSON
  /ethics/verdict        (std_msgs/String)
"""

import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String, Header
from geometry_msgs.msg import Twist

# Попытка импорта ядра (если доступно)
try:
    import sys
    sys.path.append("/home/workdir/artifacts/stalion_core")
    from ethics_veto import FormalEthicalVeto
except ImportError:
    FormalEthicalVeto = None


class PneumaNode(Node):
    def __init__(self):
        super().__init__("pneuma_node")
        self.publisher_state = self.create_publisher(Float32MultiArray, "/pneuma/state", 10)
        self.publisher_status = self.create_publisher(String, "/pneuma/status", 10)
        self.publisher_verdict = self.create_publisher(String, "/ethics/verdict", 10)

        self.timer = self.create_timer(0.5, self.timer_callback)
        self.cycle = 0
        self.pneuma = 0.63
        self.dharma = 0.62
        self.intuition = 0.70
        self.chaos = 0.50

        self.get_logger().info("PneumaNode started — publishing /pneuma/state @ 2 Hz")

    def timer_callback(self):
        self.cycle += 1
        # Простая динамика (в реальной системе сюда приходит HumanCoreOmega)
        import math
        self.chaos = 0.5 + 0.26 * math.sin(self.cycle / 23.0)
        self.pneuma = max(0.1, min(0.95, 0.63 + 0.1 * math.sin(self.cycle / 40)))

        # /pneuma/state → [pneuma, dharma, intuition, chaos, cycle]
        msg = Float32MultiArray()
        msg.data = [float(self.pneuma), float(self.dharma), float(self.intuition), float(self.chaos), float(self.cycle)]
        self.publisher_state.publish(msg)

        status = {
            "cycle": self.cycle,
            "pneuma": round(self.pneuma, 4),
            "dharma": round(self.dharma, 4),
            "intuition": round(self.intuition, 4),
            "chaos": round(self.chaos, 4),
        }
        smsg = String()
        smsg.data = json.dumps(status, ensure_ascii=False)
        self.publisher_status.publish(smsg)

        # Этический вердикт (по умолчанию allow)
        vmsg = String()
        vmsg.data = json.dumps({"result": "allow", "reason": "nominal"}, ensure_ascii=False)
        self.publisher_verdict.publish(vmsg)


def main(args=None):
    rclpy.init(args=args)
    node = PneumaNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
