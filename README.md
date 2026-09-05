# PNEVMA–STALION NEXUS v1.0

Единая исследовательская AI-платформа, объединяющая наработки PnevmaCore, CORE_SINGER,
LivingSpiral, Eternal Nexus, Aeterna/13D, мультимодальность, память, рефлексию,
LLM-adapters, WebSocket, REST API и игровые bridges.

## Назначение
Research-only: AI, симуляция, мультимодальность, цифровые агенты, игры, робототехническая
симуляция и распределённые сети. Функции автономного применения оружия, целеуказания,
поражения целей и управления боевыми системами в этот продукт не входят.

## Слои
1. Constitutional/Immutable Pattern Ledger
2. Pnevma State Engine
3. Memory + RAG
4. Reflection / Multi-agent deliberation
5. LLM Adapter Mesh
6. Tool/Network Connector Mesh
7. REST + WebSocket
8. UI / game bridges
9. Observability
10. Deployment

## LLM mesh
Подключаемые провайдеры через единый интерфейс:
- Ollama
- OpenAI-compatible endpoints
- vLLM/OpenAI-compatible servers
- собственные локальные модели

## Запуск
```bash
docker compose up -d --build
```

API: http://localhost:8000
Swagger: http://localhost:8000/docs

Локально:
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
