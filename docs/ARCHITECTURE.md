# Архитектура PNEVMA–STALION NEXUS

```text
                ┌─────────────────────────────┐
                │ Web / Unity / Godot / CLI  │
                └──────────────┬──────────────┘
                               │ REST / WebSocket
                ┌──────────────▼──────────────┐
                │       API Gateway           │
                └──────────────┬──────────────┘
                               │
       ┌───────────────────────▼───────────────────────┐
       │                 NEXUS CORE                    │
       │                                               │
       │ Immutable Pattern Ledger                     │
       │ Pnevma State / Resonance / Coherence          │
       │ Memory + RAG                                   │
       │ Reflection / Deliberation                      │
       │ Safety / Research-only boundary                │
       └───────────────┬───────────────────────────────┘
                       │ Adapter Mesh
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
       Ollama     OpenAI-compatible  vLLM
          │            │             │
          └────────────┼─────────────┘
                       ▼
             external tools / AI / apps

Storage: PostgreSQL + pgvector (production target), FAISS (local target)
Transport: HTTPS, WebSocket; optional gRPC/MCP/A2A adapters
Observability: Prometheus/Grafana target
Deployment: Docker Compose → Kubernetes
