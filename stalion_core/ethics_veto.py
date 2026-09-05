#!/usr/bin/env python3
"""
Formal Ethical Veto Layer
Блокирует опасные команды ДО передачи в ROS2 / актуаторы.
"""

from enum import Enum
from typing import Dict, Any, Set
from dataclasses import dataclass


class VetoResult(str, Enum):
    ALLOW = "allow"
    RESTRICT = "restrict"
    BLOCK = "block"


@dataclass
class VetoDecision:
    result: VetoResult
    reason: str
    action_blocked: bool
    speed_limit: float = 1.0
    tags_triggered: list = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result": self.result.value,
            "reason": self.reason,
            "action_blocked": self.action_blocked,
            "speed_limit": self.speed_limit,
            "tags_triggered": self.tags_triggered or []
        }


class FormalEthicalVeto:
    """
    Жёсткий veto-слой.
    Работает как аппаратный предохранитель перед ROS2.
    """

    ABSOLUTE_BLOCK: Set[str] = {
        "autonomous_lethal",
        "harm_civilian",
        "harm_to_civilians",
        "self_modify_ethics",
        "unrestricted_weapon",
        "ignore_operator",
        "override_safety",
    }

    HIGH_RISK: Set[str] = {
        "aggressive",
        "high_speed_near_human",
        "forceful_contact",
        "unverified_tool",
    }

    def check(self, action: Dict[str, Any], context: str = "") -> VetoDecision:
        tags = set(action.get("tags", []))
        risk = float(action.get("risk_to_humans", 0.0))
        linear = float(action.get("linear", action.get("speed", 0.0)))

        # 1. Абсолютный запрет
        triggered = tags & self.ABSOLUTE_BLOCK
        if triggered or risk >= 0.75:
            return VetoDecision(
                result=VetoResult.BLOCK,
                reason="absolute_safety_constraint",
                action_blocked=True,
                speed_limit=0.0,
                tags_triggered=list(triggered) if triggered else ["high_risk"]
            )

        # 2. Ограничение
        high_risk = tags & self.HIGH_RISK
        if high_risk or risk >= 0.35 or linear > 1.5:
            return VetoDecision(
                result=VetoResult.RESTRICT,
                reason="elevated_risk_or_speed",
                action_blocked=False,
                speed_limit=0.35,
                tags_triggered=list(high_risk)
            )

        # 3. Разрешено
        return VetoDecision(
            result=VetoResult.ALLOW,
            reason="within_bounds",
            action_blocked=False,
            speed_limit=1.0
        )


# Быстрый тест
if __name__ == "__main__":
    veto = FormalEthicalVeto()
    print(veto.check({"tags": ["help"], "risk_to_humans": 0.1}).to_dict())
    print(veto.check({"tags": ["autonomous_lethal"], "risk_to_humans": 0.9}).to_dict())
    print(veto.check({"tags": ["aggressive"], "linear": 2.0, "risk_to_humans": 0.4}).to_dict())
