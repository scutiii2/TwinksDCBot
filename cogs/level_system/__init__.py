from discord.ext import commands
from .cog import LevelSystemCog

async def setup(
    bot: commands.Bot,
):
    await bot.add_cog(
        LevelSystemCog(bot),
    )