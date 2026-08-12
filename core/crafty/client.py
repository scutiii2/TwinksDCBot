from __future__ import annotations
import aiohttp
from typing import Any
from config import Config


class CraftyError(Exception):
    """Raised when the Crafty API is misconfigured, unreachable, or returns an error."""


class CraftyClient:
    """Thin async wrapper around the Crafty Controller v2 REST API."""

    VALID_ACTIONS = {
        "start_server",
        "stop_server",
        "restart_server",
        "kill_server",
    }

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not (Config.CRAFTY_BASE_URL and Config.CRAFTY_API_TOKEN and Config.CRAFTY_SERVER_ID):
            raise CraftyError(
                "Crafty isn't configured. Set CRAFTY_BASE_URL, CRAFTY_API_TOKEN, "
                "and CRAFTY_SERVER_ID in your .env file."
            )

        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(ssl=Config.CRAFTY_VERIFY_SSL)
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {Config.CRAFTY_API_TOKEN}"},
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=10),
            )
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        session = await self._get_session()
        url = f"{Config.CRAFTY_BASE_URL.rstrip('/')}{path}"

        try:
            async with session.request(method, url, **kwargs) as resp:
                payload = await resp.json(content_type=None)
        except (aiohttp.ClientError, ValueError) as exc:
            raise CraftyError(f"Could not reach Crafty: {exc}") from exc

        if payload.get("status") != "ok":
            raise CraftyError(payload.get("error") or "Unknown Crafty API error.")

        return payload

    async def stats(self, server_id: str | None = None) -> dict[str, Any]:
        """GET /servers/{id}/stats — running state, online/max players, version, etc."""
        server_id = server_id or Config.CRAFTY_SERVER_ID
        return await self._request("GET", f"/api/v2/servers/{server_id}/stats")

    async def action(self, action: str, server_id: str | None = None) -> None:
        """POST /servers/{id}/action/{action} — start/stop/restart/kill."""
        if action not in self.VALID_ACTIONS:
            raise ValueError(f"Unsupported Crafty action: {action}")
        server_id = server_id or Config.CRAFTY_SERVER_ID
        await self._request("POST", f"/api/v2/servers/{server_id}/action/{action}")

    async def send_command(self, command: str, server_id: str | None = None) -> None:
        """POST /servers/{id}/stdin — raw console command, no leading slash."""
        server_id = server_id or Config.CRAFTY_SERVER_ID
        await self._request(
            "POST",
            f"/api/v2/servers/{server_id}/stdin",
            data=command,
            headers={"Content-Type": "text/plain"},
        )