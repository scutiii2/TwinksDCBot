from __future__ import annotations
import discord
from discord import app_commands


def is_bot_owner():
    """Restrict a slash command to the bot's owner(s)."""
    async def predicate(interaction: discord.Interaction) -> bool:
        is_owner = await interaction.client.is_owner(interaction.user)
        if not is_owner:
            await interaction.response.send_message(
                "🚫 Only the bot owner can use this command.",
                ephemeral=True,
            )
        return is_owner
    return app_commands.check(predicate)