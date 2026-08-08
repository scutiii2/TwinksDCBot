from __future__ import annotations
import asyncio
import discord
from discord.ext import commands
from config import Config
import logging
from core.logging import setup_logging
from core.guild import guild_setup
from core.ui.message import PublicMessage

class Twinks(commands.Bot):
    def __init__(self):
        self.logger = logging.getLogger("Twinks")
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):
        self.logger.info("Loading moderation extension...")
        await self.load_extension("cogs.moderation")
        self.logger.info("Moderation extension loaded.")
        self.logger.info("Syncing application commands...")
        synced = await self.tree.sync()
        for command in synced:
            self.logger.info(
                "Command: %s | ID: %s",
                command.name,
                command.id,
            )
        self.logger.info("Synced %d application commands.", len(synced))
        for guild in self.guilds:
            await guild_setup.ensure(guild)

    async def close(self):
        from core.database import database
        await database.close()
        await super().close()
        
    async def on_ready(self):
        for guild in self.guilds:
            channel = await guild_setup.logs_channel(
                guild
            )
            await (
                PublicMessage(
                    title="🟢 Twinks Online",
                    color=discord.Color.green(),
                )
                .add_field(
                    title="Guild",
                    value=guild.name,
                )
                .add_field(
                    title="Latency",
                    value=f"{round(self.latency * 1000)} ms",
                )
                .channel(channel)
            )
        
        self.logger.info("----------------------------------------")
        self.logger.info("Twinks is now online!")
        self.logger.info("Logged in as %s", self.user)
        self.logger.info("User ID: %s", self.user.id)
        self.logger.info("Guilds: %d", len(self.guilds))
        self.logger.info("----------------------------------------")
        
    async def on_guild_join(
        self,
        guild: discord.Guild,
    ):
        await guild_setup.ensure(guild)
        self.logger.info(
            "Configured %s",
            guild.name,
        )


async def main():
    setup_logging(Config.LOG_PATH)
    bot = Twinks()
    async with bot:
        await bot.start(
            Config.BOT_TOKEN
        )


if __name__ == "__main__":
    asyncio.run(main())