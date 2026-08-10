from __future__ import annotations
import discord
from discord import app_commands
from core.ui import EphemeralMessage
from .service import LevelSystemService

_service = LevelSystemService()

def registered_only():
    """Require the invoking member to be registered in the level system."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if await _service.is_registered(interaction.user.id, interaction.guild.id):
            return True

        await EphemeralMessage(
            title="📋 You're not registered yet.",
            description="Use `/register` to start tracking your level and XP.",
            color=discord.Color.orange(),
        ).send(interaction)
        return False

    return app_commands.check(predicate)