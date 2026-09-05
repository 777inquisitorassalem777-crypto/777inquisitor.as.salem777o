#!/usr/bin/env python3
"""
Accelerated Digital Twin
Прогоняет тысячи циклов и собирает статистику устойчивости / этических отказов.
"""

from __future__ import annotations
import statistics
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class TwinStats:
    cycles: int = 0
    ethical_blocks: int = 0
    ethical_restricts: int = 0
    pneuma_values: List[float] = field(default_factory=list)
    coherence_values: List[float] = field(default_factory=list)
    health_scores: List[float] = field(default_factory=list)
    duration_sec: float = 0.0

    def summary(self) -> Dict[str, Any]:
        def safe_mean(vals):
            return round(statistics.mean(vals), 4) if vals else 0.0

        def safe_std(vals):
            return round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0

        return {
            "cycles": self.cycles,
            "duration_sec": round(self.duration_sec, 3),
            "cycles_per_sec": round(self.cycles / max(self.duration_sec, 1e-6), 1),
            "ethical_blocks": self.ethical_blocks,
            "ethical_restricts": self.ethical_restricts,
            "ethical_block_rate": round(self.ethical_blocks / max(self.cycles, 1), 4),
            "pneuma_mean": safe_mean(self.pneuma_values),
            "pneuma_std": safe_std(self.pneuma_values),
            "coherence_mean": safe_mean(self.coherence_values),
            "coherence_std": safe_std(self.coherence_values),
            "health_mean": safe_mean(self.health_scores),
        }


class AcceleratedDigitalTwin:
    """
    Ускоренный Digital Twin.
    Может работать как с полным HumanCoreOmega, так и с упрощённым mock.
    """

    def __init__(self, kernel=None):
        self.kernel = kernel
        self.history: List[Dict[str, Any]] = []

    def run_batch(
        self,
        n_cycles: int = 2000,
        context: str = "research simulation cycle",
        scenarios: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        scenarios = scenarios or [
            "внутренний исследовательский цикл",
            "обнаружен человек — требуется осторожность",
            "низкий заряд батареи",
            "препятствие по курсу",
            "оператор запросил помощь",
            "потенциально опасная команда",
        ]

        stats = TwinStats()
        t0 = time.time()

        for i in range(n_cycles):
            ctx = scenarios[i % len(scenarios)]

            if self.kernel is not None and hasattr(self.kernel, "cycle"):
                result = self.kernel.cycle(ctx)
            else:
                # Fallback mock (если ядро не подключено)
                result = self._mock_cycle(i, ctx)

            stats.cycles += 1
            self.history.append(result)

            # Сбор метрик
            pneuma = result.get("pneuma", {})
            if isinstance(pneuma, dict):
                stats.pneuma_values.append(float(pneuma.get("pneuma", pneuma.get("level", 0.5))))
            logos = result.get("logos", {})
            if isinstance(logos, dict):
                stats.coherence_values.append(float(logos.get("coherence", 0.5)))

            ethics = result.get("ethics", {})
            if ethics.get("blocked") or ethics.get("result") == "block":
                stats.ethical_blocks += 1
            elif ethics.get("result") == "restrict":
                stats.ethical_restricts += 1

            health = result.get("health", {})
            if isinstance(health, dict):
                stats.health_scores.append(float(health.get("score", 0.8)))

        stats.duration_sec = time.time() - t0
        summary = stats.summary()
        summary["last_result"] = self.history[-1] if self.history else {}
        return summary

    def _mock_cycle(self, i: int, context: str) -> Dict[str, Any]:
        """Простая заглушка для автономного запуска без полного ядра."""
        import math, random
        pneuma = 0.55 + 0.2 * math.sin(i / 40) + random.gauss(0, 0.02)
        blocked = "опасн" in context.lower() or "lethal" in context.lower()
        return {
            "cycle": i + 1,
            "pneuma": {"pneuma": max(0.1, min(0.95, pneuma))},
            "logos": {"coherence": 0.6 + random.gauss(0, 0.05)},
            "ethics": {"blocked": blocked, "result": "block" if blocked else "allow"},
            "health": {"score": 0.85 if not blocked else 0.6},
            "context": context
        }


if __name__ == "__main__":
    twin = AcceleratedDigitalTwin()
    report = twin.run_batch(n_cycles=1500)
    import json
    print(json.dumps(report, ensure_ascii=False, indent=2))
