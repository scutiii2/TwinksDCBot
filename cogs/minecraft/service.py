'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
import json
from core.crafty import crafty_client
from core.numbers import bytes_to_human_readable

'''
===============================================================================
# &&Class MinecraftService
#   Middle man between the cog (talks to UI) and the Crafty API client
===============================================================================
'''
class MinecraftService:
# -----------------------------------------------------------------------------
# &&Method get_status
#   Returns a normalized status dict for the managed server
# -----------------------------------------------------------------------------
    async def get_status(self) -> dict:
        stats = await crafty_client.stats()
        data = stats.get("data")
        # info = data.get("server_id")
            
        players = data.get("players") or []
        if isinstance(players, str):
            try:
                players = json.loads(players)
            except (json.JSONDecodeError, TypeError):
                players = []
        
        return {
            "running": data.get("running"),
            "online": data.get("online") or 0,
            "max": data.get("max") or 0,
            "players": players,
            "version": data.get("version") or "Unknown",
            "cpu": data.get("cpu"),
            "mem": bytes_to_human_readable(data.get("mem")),
            "world_name": data.get("world_name"),
        }

# -----------------------------------------------------------------------------
# &&Method start / stop / restart
#   Server lifecycle actions
# -----------------------------------------------------------------------------
    async def start(self) -> None:
        await crafty_client.action("start_server")

    async def stop(self) -> None:
        await crafty_client.action("stop_server")

    async def restart(self) -> None:
        await crafty_client.action("restart_server")

# -----------------------------------------------------------------------------
# &&Method send_command
#   Sends a raw console command (no leading slash)
# -----------------------------------------------------------------------------
    async def send_command(self, command: str) -> None:
        await crafty_client.send_command(command)