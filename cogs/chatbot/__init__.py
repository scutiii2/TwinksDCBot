from discord.ext import commands
from .cog import ChatbotCog

async def setup(
    bot: commands.Bot,
):
    await bot.add_cog(
        ChatbotCog(bot),
    )
