'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
import discord
from discord import app_commands
from discord.ext import commands
from core.ui import EphemeralMessage, safe_defer
from core.discord import is_bot_owner
from core.ollama import OllamaError
from .service import ChatbotService
from .checks import allowed_guild_only

'''
===============================================================================
# &&Class ChatbotCog
#   Fun-toy AI chat backed by a self-hosted Ollama instance
#   Stateless - no conversation memory between calls
#   Talks to UI
===============================================================================
'''
class ChatbotCog(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
    ):
        self.bot = bot
        self.service = ChatbotService()

# -----------------------------------------------------------------------------
# &&Method ask
#   Sends a prompt to Ollama and replies with the generated response
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="ask",
        description="Ask the chatbot something."
    )
    @allowed_guild_only()
    async def ask(
        self,
        interaction: discord.Interaction,
        prompt: app_commands.Range[str, 1, 500],
    ):
        await safe_defer(interaction)

        try:
            response = await self.service.ask(prompt)
        except OllamaError as exc:
            await EphemeralMessage(
                title="⚠️ Couldn't reach the chatbot.",
                description=str(exc),
                color=discord.Color.red(),
            ).followup(interaction)
            return

        embed = discord.Embed(
            description=response[:4000],
            color=discord.Color.blurple(),
        )
        embed.set_footer(text=f"Asked by {interaction.user.display_name}")

        await interaction.followup.send(embed=embed)

# -----------------------------------------------------------------------------
# &&Method addserver
#   Whitelists a server for the chatbot (owner only).
#   Defaults to the current server if no guild_id is given.
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="addserver",
        description="Allow a server to use the chatbot. (Owner only)"
    )
    @is_bot_owner()
    async def addserver(
        self,
        interaction: discord.Interaction,
        guild_id: str | None = None,
    ):
        target_id = interaction.guild.id
        if guild_id is not None:
            if not guild_id.isdigit():
                await EphemeralMessage(
                    title="⚠️ Invalid server ID.",
                    color=discord.Color.red(),
                ).send(interaction)
                return
            target_id = int(guild_id)

        added = await self.service.add_guild(target_id, interaction.user.id)
        message = (
            EphemeralMessage(
                title=f"✅ Server `{target_id}` added.",
                color=discord.Color.green(),
            )
            if added else
            EphemeralMessage(
                title=f"Server `{target_id}` is already allowed.",
                color=discord.Color.orange(),
            )
        )
        await message.send(interaction)

# -----------------------------------------------------------------------------
# &&Method removeserver
#   Un-whitelists a server (owner only).
#   Defaults to the current server if no guild_id is given.
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="removeserver",
        description="Remove a server's chatbot access. (Owner only)"
    )
    @is_bot_owner()
    async def removeserver(
        self,
        interaction: discord.Interaction,
        guild_id: str | None = None,
    ):
        target_id = interaction.guild.id
        if guild_id is not None:
            if not guild_id.isdigit():
                await EphemeralMessage(
                    title="⚠️ Invalid server ID.",
                    color=discord.Color.red(),
                ).send(interaction)
                return
            target_id = int(guild_id)

        removed = await self.service.remove_guild(target_id)
        message = (
            EphemeralMessage(
                title=f"✅ Server `{target_id}` removed.",
                color=discord.Color.green(),
            )
            if removed else
            EphemeralMessage(
                title=f"Server `{target_id}` wasn't in the allowed list.",
                color=discord.Color.orange(),
            )
        )
        await message.send(interaction)
