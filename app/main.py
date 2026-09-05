from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from .core import NexusCore

app = FastAPI(title="PNEVMA–STALION NEXUS", version="1.0.0")
core = NexusCore()

class ChatRequest(BaseModel):
    message: str
    provider: str = "auto"

class MemoryRequest(BaseModel):
    text: str
    metadata: dict = {}

@app.get("/health")
def health():
    return {"status": "ok", "product": "pnevma-stalion-nexus", "version": "1.0.0"}

@app.get("/patterns")
def patterns():
    return core.patterns.manifest()

@app.post("/chat")
async def chat(req: ChatRequest):
    return await core.chat(req.message, req.provider)

@app.post("/memory")
def memory(req: MemoryRequest):
    return core.memory.add(req.text, req.metadata)

@app.get("/memory/search")
def memory_search(q: str, k: int = 5):
    return {"results": core.memory.search(q, k)}

@app.get("/reflection")
def reflection():
    return core.reflection.snapshot()

@app.websocket("/ws/metrics")
async def metrics(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json(core.metrics())
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
