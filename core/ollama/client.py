from __future__ import annotations
import aiohttp
from config import Config


class OllamaError(Exception):
    """Raised when Ollama is unreachable, misconfigured, or returns an error."""


class OllamaClient:
    """Thin async wrapper around the Ollama REST API (stateless, single-turn)."""

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not Config.OLLAMA_BASE_URL:
            raise OllamaError(
                "Ollama isn't configured. Set OLLAMA_BASE_URL in your .env file."
            )

        if self._session is None or self._session.closed:
            # Generous timeout - CPU inference on modest hardware can be slow,
            # especially on a "cold" request after the model has idled out.
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120),
            )
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
        system: str | None = None,
    ) -> str:
        """POST /api/generate - single-turn, stateless completion. No conversation memory.

        `system` sets the model's persona/identity for this single call (Ollama
        re-applies it fresh each request since there's no session state kept
        between calls).
        """
        session = await self._get_session()
        model = model or Config.OLLAMA_MODEL

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        url = f"{Config.OLLAMA_BASE_URL.rstrip('/')}/api/generate"

        try:
            async with session.post(url, json=payload) as resp:
                data = await resp.json(content_type=None)
        except (aiohttp.ClientError, ValueError) as exc:
            raise OllamaError(f"Could not reach Ollama: {exc}") from exc

        if "error" in data:
            raise OllamaError(data["error"])

        response = (data.get("response") or "").strip()
        if not response:
            raise OllamaError("Ollama returned an empty response.")

        return response