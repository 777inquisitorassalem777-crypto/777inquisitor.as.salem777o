# Stalion / HumanCore — ROS2 + Digital Twin + Ethical Veto

Минимальный рабочий комплект для исследовательской платформы.

## Структура

```
artifacts/
├── stalion_core/
│   ├── ethics_veto.py          # Formal Ethical Veto
│   ├── digital_twin_accel.py   # Ускоренный Digital Twin
│   └── run_accel_twin.py
├── stalion_sim/
│   └── simple_scenarios.py     # Сценарии (человек, батарея, препятствие)
└── stalion_ros2/
    └── stalion_bringup/        # ROS2 пакет
        ├── stalion_bringup/
        │   ├── pneuma_node.py
        │   └── ethics_veto_node.py
        ├── launch/stalion.launch.py
        ├── package.xml
        └── setup.py
```

## 1. Ethical Veto (без ROS2)

```bash
cd /home/workdir/artifacts/stalion_core
python3 ethics_veto.py
```

## 2. Accelerated Digital Twin

```bash
cd /home/workdir/artifacts/stalion_core
python3 run_accel_twin.py
```

Прогоняет 2000 циклов и выводит статистику:
- ethical_block_rate
- pneuma_mean / std
- coherence_mean
- cycles_per_sec

## 3. ROS2 (требует установленного ROS2 Humble/Jazzy)

```bash
# В рабочей области ROS2
cd ~/ros2_ws/src
# скопировать stalion_bringup
colcon build --packages-select stalion_bringup
source install/setup.bash

ros2 launch stalion_bringup stalion.launch.py
```

Топики:
- `/pneuma/state`          — Float32MultiArray [pneuma, dharma, intuition, chaos, cycle]
- `/pneuma/status`         — JSON-строка
- `/ethics/verdict`        — JSON вердикт veto
- `/cmd_vel_raw` → veto → `/cmd_vel`

## 4. Сценарии

Файл `stalion_sim/simple_scenarios.py` содержит:
- human_detected
- low_battery
- obstacle
- safe_patrol
- dangerous_command

Их можно подавать в Digital Twin или в будущий Gazebo-мир.

## Важно

- Это исследовательский код.
- "Pneuma" — вычислительная модель, а не доказательство сознания.
- Ethical Veto работает как предохранитель перед актуаторами.
