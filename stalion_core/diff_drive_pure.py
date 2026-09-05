#!/usr/bin/env python3
"""
Чистый дифференциальный контроллер (без ROS2).
Можно использовать в Digital Twin / симуляции / тестах.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Pose2D:
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0  # рад


class DiffDriveController:
    """
    Дифференциальный привод.

    Параметры по умолчанию соответствуют URDF Stalion:
      wheel_separation = 0.60 м
      wheel_radius     = 0.12 м
    """

    def __init__(
        self,
        wheel_separation: float = 0.60,
        wheel_radius: float = 0.12,
        max_linear: float = 1.0,
        max_angular: float = 2.0,
    ):
        self.L = wheel_separation
        self.r = wheel_radius
        self.max_linear = max_linear
        self.max_angular = max_angular
        self.pose = Pose2D()

    def twist_to_wheels(self, linear: float, angular: float) -> Tuple[float, float]:
        """
        Преобразование (v, ω) → (ω_left, ω_right) [рад/с]
        """
        linear = max(-self.max_linear, min(self.max_linear, linear))
        angular = max(-self.max_angular, min(self.max_angular, angular))

        half_l = self.L / 2.0
        v_left = (linear - angular * half_l) / self.r
        v_right = (linear + angular * half_l) / self.r
        return v_left, v_right

    def wheels_to_twist(self, w_left: float, w_right: float) -> Tuple[float, float]:
        """
        Обратное преобразование (ω_left, ω_right) → (v, ω)
        """
        linear = self.r * (w_left + w_right) / 2.0
        angular = self.r * (w_right - w_left) / self.L
        return linear, angular

    def step(self, linear: float, angular: float, dt: float) -> Pose2D:
        """
        Один шаг интегрирования одометрии.
        Возвращает новую позу.
        """
        linear = max(-self.max_linear, min(self.max_linear, linear))
        angular = max(-self.max_angular, min(self.max_angular, angular))

        self.pose.x += linear * math.cos(self.pose.theta) * dt
        self.pose.y += linear * math.sin(self.pose.theta) * dt
        self.pose.theta += angular * dt
        self.pose.theta = math.atan2(
            math.sin(self.pose.theta), math.cos(self.pose.theta)
        )
        return self.pose

    def reset(self, x: float = 0.0, y: float = 0.0, theta: float = 0.0):
        self.pose = Pose2D(x, y, theta)


# ---------------------------------------------------------------------------
# Быстрый тест
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ctrl = DiffDriveController()

    print("=== Diff Drive Controller Test ===")
    print(f"Wheel separation: {ctrl.L} m")
    print(f"Wheel radius:     {ctrl.r} m\n")

    # Прямо
    wl, wr = ctrl.twist_to_wheels(0.5, 0.0)
    print(f"v=0.5, ω=0.0  →  left={wl:.3f} rad/s  right={wr:.3f} rad/s")

    # Поворот на месте
    wl, wr = ctrl.twist_to_wheels(0.0, 1.0)
    print(f"v=0.0, ω=1.0  →  left={wl:.3f} rad/s  right={wr:.3f} rad/s")

    # Дуга
    wl, wr = ctrl.twist_to_wheels(0.4, 0.5)
    print(f"v=0.4, ω=0.5  →  left={wl:.3f} rad/s  right={wr:.3f} rad/s")

    # Интегрирование 2 секунды вперёд
    print("\nИнтегрирование 2.0 с при v=0.5:")
    for _ in range(20):
        pose = ctrl.step(0.5, 0.0, 0.1)
    print(f"  pose → x={pose.x:.3f}  y={pose.y:.3f}  θ={math.degrees(pose.theta):.1f}°")
