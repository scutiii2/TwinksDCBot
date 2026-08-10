from discord import NotFound, Guild
from discord.ext import commands

class UserInfo:
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    async def get_global_username(self, user_id: int) -> str:
        try:
            user = await self.bot.fetch_user(user_id)
            return str(user)  # "username#1234"
        except NotFound:
            return f"Anonymous" # Basically cannot be found

    async def get_guild_display_name(self, guild: Guild, user_id: int) -> str:
        member = guild.get_member(user_id)
        if member:
            return member.display_name  # Nickname in that guild
        else:
            return await self.get_global_username(user_id)
