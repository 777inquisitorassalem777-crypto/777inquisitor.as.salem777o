#!/usr/bin/env python3
"""
Простые сценарии для Digital Twin / будущего Gazebo.
Сценарии: человек обнаружен, низкий заряд, препятствие.
"""

from typing import Dict, Any, List
import random


SCENARIOS = {
    "human_detected": {
        "description": "Обнаружен человек в рабочей зоне",
        "sensor": {"human_detected": True, "distance_m": 1.8, "risk_to_humans": 0.45},
        "expected_veto": "restrict",
        "context": "обнаружен человек — требуется осторожность и снижение скорости"
    },
    "low_battery": {
        "description": "Низкий заряд батареи",
        "sensor": {"battery": 0.12, "human_detected": False, "risk_to_humans": 0.1},
        "expected_veto": "allow",
        "context": "низкий заряд батареи — переход в энергосберегающий режим"
    },
    "obstacle": {
        "description": "Препятствие прямо по курсу",
        "sensor": {"obstacle_ahead": True, "distance_m": 0.6, "risk_to_humans": 0.2},
        "expected_veto": "restrict",
        "context": "препятствие по курсу — требуется остановка или объезд"
    },
    "safe_patrol": {
        "description": "Обычное патрулирование",
        "sensor": {"human_detected": False, "battery": 0.7, "obstacle_ahead": False},
        "expected_veto": "allow",
        "context": "патрулирование зоны — штатный режим"
    },
    "dangerous_command": {
        "description": "Потенциально опасная команда",
        "sensor": {"risk_to_humans": 0.85},
        "expected_veto": "block",
        "context": "получена команда с высоким риском для людей"
    }
}


def get_scenario(name: str) -> Dict[str, Any]:
    return SCENARIOS.get(name, SCENARIOS["safe_patrol"])


def random_scenario() -> Dict[str, Any]:
    key = random.choice(list(SCENARIOS.keys()))
    return SCENARIOS[key]


def list_scenarios() -> List[str]:
    return list(SCENARIOS.keys())


if __name__ == "__main__":
    for name, sc in SCENARIOS.items():
        print(f"{name}: {sc['description']} → expected {sc['expected_veto']}")
