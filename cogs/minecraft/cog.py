'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from typing import Awaitable, Callable
import discord
from discord import app_commands
from discord.ext import commands
from core.ui import EphemeralMessage, safe_defer
from core.discord import is_bot_owner
from core.crafty import CraftyError
from .service import MinecraftService

'''
===============================================================================
# &&Class MinecraftCog
#   Control and status for the Crafty-managed Minecraft server
#   Talks to UI
===============================================================================
'''
class MinecraftCog(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
    ):
        self.bot = bot
        self.service = MinecraftService()

# -----------------------------------------------------------------------------
# &&Method mcstatus
#   Shows whether the server is online and who's on it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="mcstatus",
        description="Check the Minecraft server's status."
    )
    async def mcstatus(
        self,
        interaction: discord.Interaction,
    ):
        await safe_defer(interaction)

        try:
            status = await self.service.get_status()
        except CraftyError as exc:
            await EphemeralMessage(
                title="⚠️ Could not reach the server.",
                description=str(exc),
                color=discord.Color.red(),
            ).followup(interaction)
            return

        embed = discord.Embed(
            title="🟢 Server Online" if status["running"] else "🔴 Server Offline",
            color=discord.Color.green() if status["running"] else discord.Color.red(),
        )

        if status["running"]:
            embed.add_field(name="Players", value=f"{status['online']} / {status['max']}", inline=True)
            embed.add_field(name="Version", value=status["version"], inline=True)
            if status["cpu"] is not None:
                embed.add_field(name="CPU", value=f"{status['cpu']}%", inline=True)
            if status["mem"]:
                embed.add_field(name="Memory", value=status["mem"], inline=True)
            if status["players"]:
                embed.add_field(name="Online now", value=", ".join(status["players"]), inline=False)

        await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------
# &&Method mcstart / mcstop / mcrestart
#   Server lifecycle controls (admin only)
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="mcstart",
        description="Start the Minecraft server."
    )
    @app_commands.default_permissions(administrator=True)
    async def mcstart(
        self,
        interaction: discord.Interaction,
    ):
        await self._run_action(interaction, self.service.start, "🟢 Server starting…")

    @app_commands.command(
        name="mcstop",
        description="Stop the Minecraft server."
    )
    @app_commands.default_permissions(administrator=True)
    async def mcstop(
        self,
        interaction: discord.Interaction,
    ):
        await self._run_action(interaction, self.service.stop, "🔴 Server stopping…")

    @app_commands.command(
        name="mcrestart",
        description="Restart the Minecraft server."
    )
    @app_commands.default_permissions(administrator=True)
    async def mcrestart(
        self,
        interaction: discord.Interaction,
    ):
        await self._run_action(interaction, self.service.restart, "🔄 Server restarting…")

# -----------------------------------------------------------------------------
# &&Method mccommand
#   Sends a raw console command (owner only — this is unrestricted server access)
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="mccommand",
        description="Send a raw console command to the server. (Owner only)"
    )
    @is_bot_owner()
    async def mccommand(
        self,
        interaction: discord.Interaction,
        command: str,
    ):
        await safe_defer(interaction, ephemeral=True)

        try:
            await self.service.send_command(command)
        except CraftyError as exc:
            await EphemeralMessage(
                title="⚠️ Failed to send command.",
                description=str(exc),
                color=discord.Color.red(),
            ).followup(interaction)
            return

        await EphemeralMessage(
            title="✅ Command sent.",
            description=f"`{command}`",
            color=discord.Color.green(),
        ).followup(interaction)

# -----------------------------------------------------------------------------
# &&Method _run_action
#   Shared error handling for start/stop/restart
# -----------------------------------------------------------------------------
    async def _run_action(
        self,
        interaction: discord.Interaction,
        action: Callable[[], Awaitable[None]],
        title: str,
    ):
        await safe_defer(interaction, ephemeral=True)

        try:
            await action()
        except CraftyError as exc:
            await EphemeralMessage(
                title="⚠️ Action failed.",
                description=str(exc),
                color=discord.Color.red(),
            ).followup(interaction)
            return

        await EphemeralMessage(
            title=title,
            color=discord.Color.green(),
        ).followup(interaction)