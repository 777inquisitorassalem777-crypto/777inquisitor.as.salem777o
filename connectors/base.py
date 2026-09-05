from abc import ABC, abstractmethod

class AIConnector(ABC):
    name = "base"

    @abstractmethod
    async def generate(self, prompt: str, **kwargs):
        raise NotImplementedError

    async def health(self):
        return {"name": self.name, "status": "unknown"}

    def capabilities(self):
        return {"text": True}
