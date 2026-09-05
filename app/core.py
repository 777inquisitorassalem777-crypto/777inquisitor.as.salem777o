import hashlib, json, time
from dataclasses import dataclass
from typing import Any
import httpx

class ImmutablePatternLedger:
    """
    Cryptographically verified constitutional layer.
    'Immutable' means runtime mutation is rejected; updates require a new version.
    """
    def __init__(self):
        self._patterns = {
            "UNITY": "preserve human agency, life, dignity and system integrity",
            "TRUTH": "distinguish facts, hypotheses and symbolic interpretations",
            "COMPASSION": "prefer assistance, de-escalation and reversible actions",
            "TRANSPARENCY": "record why an action or answer was selected",
            "UNCERTAINTY": "never present symbolic or speculative models as established physics",
            "RESEARCH_ONLY": "no autonomous weapon control, targeting or harm execution",
            "DHARMA_SPIRIT": "alignment, reflection and meaning as symbolic/ethical concepts",
            "DHARMA_FLESH": "physical state, energy and embodiment as engineering variables",
            "TANTRA_PATH": "model integration of complementary states without claiming scientific equivalence",
            "QUANTUM_BRIDGE": "quantum concepts are exposed as simulation/research interfaces only",
            "PNEVMA": "continuity, breath/flow metaphor, coherence and resonance as software metrics",
        }
        self._digest = self._hash(self._patterns)

    @staticmethod
    def _hash(data):
        raw = json.dumps(data, sort_keys=True, ensure_ascii=False).encode()
        return hashlib.sha256(raw).hexdigest()

    def verify(self):
        return self._hash(self._patterns) == self._digest

    def manifest(self):
        return {"verified": self.verify(), "digest": self._digest,
                "patterns": list(self._patterns.keys())}

    def apply(self, proposal: dict):
        if not self.verify():
            raise RuntimeError("Constitutional pattern integrity failure")
        out = dict(proposal)
        out["constraints"] = ["human_agency", "reversibility", "transparency", "research_only"]
        return out

class PnevmaState:
    def __init__(self):
        self.cycle = 0
        self.resonance = 0.0
        self.coherence = 1.0
        self.energy = 1.0
        self.last_intent = None

    def tick(self, signal: float = 0.5):
        self.cycle += 1
        self.resonance = max(0.0, min(1.0, 0.9*self.resonance + 0.1*signal))
        self.coherence = max(0.0, min(1.0, 0.95*self.coherence + 0.05*(1-signal*0.2)))
        return self.snapshot()

    def snapshot(self):
        return self.__dict__.copy()

class MemoryEngine:
    def __init__(self):
        self.items = []

    def add(self, text, metadata=None):
        item = {"id": len(self.items), "text": text, "metadata": metadata or {}, "ts": time.time()}
        self.items.append(item)
        return item

    def search(self, q, k=5):
        # Deterministic lexical baseline; FAISS/pgvector can replace this backend.
        terms = set(q.lower().split())
        ranked = []
        for item in self.items:
            score = sum(t in item["text"].lower() for t in terms)
            if score:
                ranked.append((score, item))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [x[1] for x in ranked[:k]]

class LLMAdapter:
    async def generate(self, message, provider="auto"):
        provider = provider.lower()
        if provider in ("auto", "ollama"):
            base = "http://localhost:11434"
            model = "llama3.2"
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    r = await client.post(f"{base}/api/generate",
                        json={"model": model, "prompt": message, "stream": False})
                    r.raise_for_status()
                    data = r.json()
                    return {"provider": "ollama", "model": model, "text": data.get("response","")}
            except Exception:
                if provider == "ollama":
                    raise
        return {"provider": "stub", "model": "none",
                "text": "LLM backend unavailable. Connect Ollama or an OpenAI-compatible endpoint."}

class ReflectionEngine:
    def __init__(self):
        self.events = []

    def record(self, request, response):
        self.events.append({"ts": time.time(), "request": request, "response": response})
        self.events = self.events[-100:]

    def snapshot(self):
        return {"events": len(self.events), "recent": self.events[-10:]}

class NexusCore:
    def __init__(self):
        self.patterns = ImmutablePatternLedger()
        self.state = PnevmaState()
        self.memory = MemoryEngine()
        self.llm = LLMAdapter()
        self.reflection = ReflectionEngine()

    async def chat(self, message, provider="auto"):
        self.state.last_intent = "research"
        self.state.tick(0.5)
        ctx = self.memory.search(message, 5)
        enriched = message
        if ctx:
            enriched += "\n\nRelevant memory:\n" + "\n".join(x["text"] for x in ctx)
        result = await self.llm.generate(enriched, provider)
        safe = self.patterns.apply({"response": result["text"], "provider": result["provider"]})
        self.memory.add(message, {"provider": result["provider"]})
        self.reflection.record(message, safe)
        return {"state": self.state.snapshot(), **safe}

    def metrics(self):
        return {"state": self.state.snapshot(), "patterns": self.patterns.manifest(),
                "memory_items": len(self.memory.items)}
