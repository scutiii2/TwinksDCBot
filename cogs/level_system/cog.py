'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
import discord
from discord import app_commands, Member
from discord.ext import commands
from .service import LevelSystemService

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
# &&Method levelinfo
#   Levelinfo latest the message/s of a member
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="levelinfo",
        description="Show level information of member"
    )
    async def levelinfo(
        self,
        interaction: discord.Interaction,
        member: Member | None = None,
        show_to_everyone: bool = False
    ):
        if not member:
            member = interaction.user
            
        user_level = await self.service.get_user(member.id, interaction.guild.id)
        