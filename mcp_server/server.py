from __future__ import annotations
import asyncio
import logging
from mcp.server.mcpserver import MCPServer
from cogs.minecraft.service import MinecraftService
from cogs.level_system.service import LevelSystemService
from config import Config

logger = logging.getLogger("Twinks.mcp")

mcp = MCPServer("twinks")


@mcp.tool()
async def mc_start() -> dict[str, str]:
    """Start the managed Minecraft server."""
    await MinecraftService().start()
    return {"status": "start requested"}


@mcp.tool()
async def leaderboard(
    guild_id: int,
    overall: bool = False,
    count: int = 10,
) -> list[dict]:
    """Get the level/XP leaderboard for a guild, or the global leaderboard if overall=True."""
    return await LevelSystemService().get_top_users(guild_id, overall=overall, count=count)


_task: asyncio.Task | None = None


async def start() -> None:
    global _task
    _task = asyncio.create_task(
        mcp.run_streamable_http_async(host=Config.MCP_HOST, port=Config.MCP_PORT)
    )
    logger.info("MCP server listening on %s:%d", Config.MCP_HOST, Config.MCP_PORT)


async def stop() -> None:
    global _task
    if _task is not None:
        _task.cancel()
        _task = None
