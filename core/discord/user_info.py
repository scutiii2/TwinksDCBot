from discord import NotFound, Guild
from discord.ext import commands


class UserInfo:
    """Resolves Discord IDs into readable names."""

    async def get_global_username(self, bot: commands.Bot, user_id: int) -> str:
        try:
            user = await bot.fetch_user(user_id)
            return str(user)  # "username"
        except NotFound:
            return "Unknown User"

    async def get_guild_display_name(self, bot: commands.Bot, guild: Guild, user_id: int) -> str:
        member = guild.get_member(user_id)
        if member:
            return member.display_name  # nickname in that guild
        return await self.get_global_username(bot, user_id)