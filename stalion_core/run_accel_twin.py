#!/usr/bin/env python3
"""
Запуск ускоренного Digital Twin + отчёт.
"""

import json
import sys
sys.path.append("/home/workdir/artifacts/stalion_core")
sys.path.append("/home/workdir/artifacts/stalion_sim")

from digital_twin_accel import AcceleratedDigitalTwin
from simple_scenarios import SCENARIOS

def main():
    print("=" * 60)
    print(" Accelerated Digital Twin — Stalion / HumanCore")
    print("=" * 60)

    twin = AcceleratedDigitalTwin(kernel=None)  # mock mode
    scenarios = [sc["context"] for sc in SCENARIOS.values()]

    report = twin.run_batch(n_cycles=2000, scenarios=scenarios)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\nГотово. Для подключения реального ядра передайте kernel=HumanCoreOmega()")

if __name__ == "__main__":
    main()
