from .client import OllamaClient, OllamaError

ollama_client = OllamaClient()

__all__ = (
    "ollama_client",
    "OllamaError",
)
