from __future__ import annotations
import discord
from discord import app_commands
from core.ui import EphemeralMessage, safe_defer
from .service import ChatbotService

_service = ChatbotService()

def allowed_guild_only():
    """Require the invoking guild to be whitelisted for the chatbot.

    Defers FIRST, before the whitelist DB lookup. Checks run before the
    command body, so if we wait to defer inside the command itself, this
    check's own I/O eats into Discord's 3-second ack window and can expire
    the interaction before the command ever gets a chance to defer -
    every followup.send() after that 404s with "Unknown Webhook".
    """
    async def predicate(interaction: discord.Interaction) -> bool:
        await safe_defer(interaction)

        if await _service.is_allowed(interaction.guild.id):
            return True

        await EphemeralMessage(
            title="🚫 This server isn't enabled for the chatbot.",
            description="Ask the bot owner to enable it with `/addserver`.",
            color=discord.Color.orange(),
        ).followup(interaction)
        return False

    return app_commands.check(predicate)