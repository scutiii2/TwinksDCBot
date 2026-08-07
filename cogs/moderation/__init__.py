from discord.ext import commands

from .cog import ModerationCog


async def setup(
    bot: commands.Bot,
):

    await bot.add_cog(
        ModerationCog(bot),
    )