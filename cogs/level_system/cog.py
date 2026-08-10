'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
import discord
from discord import app_commands, Member
from discord.ext import commands
from core.ui import EphemeralMessage, safe_defer
from core.discord import user_info
from .service import LevelSystemService
from .checks import registered_only
from .leveling import xp_progress

'''
===============================================================================
# &&Class LevelSystem Cog
#   For user types Level System
#   Talks to UI
===============================================================================
'''
class LevelSystemCog(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
    ):
        self.bot = bot
        self.service = LevelSystemService()

# -----------------------------------------------------------------------------
# &&Method register
#   Registers the invoking member into the level system
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="register",
        description="Register yourself for the level system."
    )
    async def register(
        self,
        interaction: discord.Interaction,
    ):
        created = await self.service.register(interaction.user.id, interaction.guild.id)
        message = (
            EphemeralMessage(
                title="✅ Registered!",
                description="You're all set. Start earning XP around the server.",
                color=discord.Color.green(),
            )
            if created else
            EphemeralMessage(
                title="You're already registered.",
                color=discord.Color.orange(),
            )
        )
        await message.send(interaction)

# -----------------------------------------------------------------------------
# &&Method levelinfo
#   Shows level information of a member
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="levelinfo",
        description="Show level information of a member."
    )
    @registered_only()
    async def levelinfo(
        self,
        interaction: discord.Interaction,
        member: Member | None = None,
        show_to_everyone: bool = False,
    ):
        member = member or interaction.user
        user = await self.service.get_user(member.id, interaction.guild.id)
        if user is None:
            await EphemeralMessage(
                title=f"{member.display_name} hasn't registered yet.",
                color=discord.Color.red(),
            ).send(interaction)
            return

        level, into_level, needed = xp_progress(user["xp"])
        embed = discord.Embed(
            title=f"{member.display_name}'s Level",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Level", value=str(level), inline=True)
        embed.add_field(name="Total XP", value=str(user["xp"]), inline=True)
        embed.add_field(
            name="Progress",
            value=f"{into_level} / {needed} XP to next level",
            inline=False,
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=not show_to_everyone,
        )
        
# -----------------------------------------------------------------------------
# &&Method leaderboard
#   Shows the top members by XP
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="leaderboard",
        description="Show the XP leaderboard."
    )
    @registered_only()
    async def leaderboard(
        self,
        interaction: discord.Interaction,
        overall: bool = False,
        show_to_everyone: bool = False,
    ):
        await safe_defer(interaction, ephemeral = not show_to_everyone)

        top_users = await self.service.get_top_users(
            interaction.guild.id,
            overall=overall,
        )

        embed = discord.Embed(
            title="🏆 Overall Leaderboard" if overall else "🏆 Server Leaderboard",
            color=discord.Color.gold(),
        )

        if not top_users:
            embed.description = "No one has earned XP yet."
        else:
            lines = []
            for i, row in enumerate(top_users, start=1):
                name = await user_info.get_guild_display_name(
                    self.bot, interaction.guild, row["user_id"]
                )
                lines.append(f"**#{i}** {name} — Level {row['level']} ({row['xp']} XP)")
            embed.description = "\n".join(lines)

        await interaction.followup.send(
            embed=embed,
            ephemeral=not show_to_everyone,
        )