from discord.ext import commands
from .cog import OwnerCog

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerCog(bot))