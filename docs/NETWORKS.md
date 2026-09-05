# Сопряжение с AI и сетями

## Единый контракт адаптера

Каждый внешний AI подключается через:

- `generate(request) -> response`
- `health()`
- `capabilities()`

## Поддерживаемые классы

1. Local AI: Ollama
2. OpenAI-compatible API: любой сервер с совместимым `/v1` API
3. vLLM: через OpenAI-compatible интерфейс
4. Game engines: WebSocket/HTTP bridge
5. Future: MCP/A2A adapters
6. Messaging: Matrix/other gateways через отдельный connector service

## Правило безопасности

Сетевые адаптеры получают только разрешённые capabilities. Нельзя давать внешнему
агенту прямой доступ к исполнительным системам. Для робототехнических экспериментов
используется sandbox/simulator adapter.
