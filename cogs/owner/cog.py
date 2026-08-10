'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
import discord
from discord import app_commands
from discord.ext import commands
from core.discord import is_bot_owner

'''
===============================================================================
# &&Class OwnerCog
#   Bot-owner-only utilities: shutdown, guild inspection
#   Talks to UI
===============================================================================
'''
class OwnerCog(commands.Cog):

    # Permissions worth surfacing per-guild (keeps the report readable)
    KEY_PERMISSIONS = (
        "administrator",
        "manage_guild",
        "manage_roles",
        "manage_channels",
        "manage_messages",
        "kick_members",
        "ban_members",
        "moderate_members",
        "view_audit_log",
    )

    # Baseline permissions the bot needs to actually function
    REQUIRED_PERMISSIONS = (
        "view_channel",
        "send_messages",
        "embed_links",
        "read_message_history",
    )

    def __init__(self, bot: commands.Bot):
        self.bot = bot

# -----------------------------------------------------------------------------
# &&Method shutdowntwinks
#   Gracefully closes the bot (owner only, requires confirmation)
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="shutdowntwinks",
        description="Shut down the bot. (Owner only)"
    )
    @is_bot_owner()
    async def shutdowntwinks(
        self,
        interaction: discord.Interaction,
    ):
        view = _ConfirmShutdown(self.bot)
        await interaction.response.send_message(
            "⚠️ This will shut down the bot for **all** servers. Are you sure?",
            view=view,
            ephemeral=True,
        )

# -----------------------------------------------------------------------------
# &&Method servers
#   Lists every guild the bot is in and its permissions there
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="servers",
        description="List all servers the bot is in and its permissions. (Owner only)"
    )
    @is_bot_owner()
    async def servers(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.defer(ephemeral=True)

        guilds = sorted(
            self.bot.guilds,
            key=lambda g: g.member_count or 0,
            reverse=True,
        )

        if not guilds:
            await interaction.followup.send("Not in any servers.", ephemeral=True)
            return

        for embed in self._build_embeds(guilds):
            await interaction.followup.send(embed=embed, ephemeral=True)

# -----------------------------------------------------------------------------
# &&Method _build_embeds
#   Chunks guilds into embeds (Discord caps embeds at 25 fields)
# -----------------------------------------------------------------------------
    def _build_embeds(
        self,
        guilds: list[discord.Guild],
    ) -> list[discord.Embed]:
        embeds = []
        chunks = [guilds[i:i + 25] for i in range(0, len(guilds), 25)]

        for chunk in chunks:
            embed = discord.Embed(
                title=f"🌐 Servers ({len(guilds)})",
                color=discord.Color.blurple(),
            )
            for guild in chunk:
                embed.add_field(
                    name=f"{guild.name} ({guild.id})",
                    value=self._describe_permissions(guild),
                    inline=False,
                )
            embeds.append(embed)

        return embeds

# -----------------------------------------------------------------------------
# &&Method _describe_permissions
#   Human-readable summary of the bot's permissions in a guild
# -----------------------------------------------------------------------------
    def _describe_permissions(
        self,
        guild: discord.Guild,
    ) -> str:
        perms = guild.me.guild_permissions
        lines = [f"👥 {guild.member_count} members"]

        if perms.administrator:
            lines.append("✅ Administrator (all permissions granted)")
            return "\n".join(lines)

        granted = [
            p.replace("_", " ").title()
            for p in self.KEY_PERMISSIONS
            if getattr(perms, p)
        ]
        lines.append("✅ " + ", ".join(granted) if granted else "⚠️ No key permissions granted")

        missing_required = [
            p.replace("_", " ").title()
            for p in self.REQUIRED_PERMISSIONS
            if not getattr(perms, p)
        ]
        if missing_required:
            lines.append(f"🚫 Missing required: {', '.join(missing_required)}")

        return "\n".join(lines)


'''
===============================================================================
# &&Class _ConfirmShutdown
#   Ephemeral confirm/cancel view guarding the shutdown command
===============================================================================
'''
class _ConfirmShutdown(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=30)
        self.bot = bot

    @discord.ui.button(label="Shut down", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="🔴 Shutting down...", view=self)
        await self.bot.close()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="Shutdown cancelled.", view=self)

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True