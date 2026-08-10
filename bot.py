from __future__ import annotations
import asyncio
import logging
import discord
from discord.ext import commands
from core.process_lock import acquire, release
from core.logging import setup_logging
from core.guild import guild_setup, prefix_service
from core.ui import PublicMessage
from cogs import COGS
from config import Config


async def get_prefix(bot: commands.Bot, message: discord.Message):
    if message.guild is None:
        return commands.when_mentioned_or("!")(bot, message)
    prefix = await prefix_service.get(message.guild.id)
    return commands.when_mentioned_or(prefix)(bot, message)

class Twinks(commands.Bot):
    def __init__(self):
        self.logger = logging.getLogger("Twinks")
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
        )

    async def _load_cogs(self):
        for name, enabled in COGS.items():
            if not enabled:
                self.logger.info("Skipping disabled extension: %s", name)
                continue

            try:
                await self.load_extension(f"cogs.{name}")
                self.logger.info("Loaded extension: %s", name)
            except commands.ExtensionError:
                self.logger.exception("Failed to load extension: %s", name)

    async def setup_hook(self):
        await self._load_cogs()
        
        @self.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
            if isinstance(error, discord.app_commands.CheckFailure):
                return  # already handled inside the check itself
            self.logger.exception("Unhandled app command error", exc_info=error)

        if Config.DEV_GUILD_ID:
            guild = discord.Object(id=Config.DEV_GUILD_ID)
            
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            self.logger.info("Synced %d application commands to dev guild.", len(synced))
        else:
            self.logger.info("Syncing application commands globally...")
            synced = await self.tree.sync()
            self.logger.info("Synced %d application commands.", len(synced))
        
        for guild in self.guilds:
            await guild_setup.ensure(guild)
            

    async def close(self):
        from core.database import databaseManager
        await databaseManager.close()
        await super().close()
        
    async def on_ready(self):
        for guild in self.guilds:
            channel = await guild_setup.logs_channel(guild)
            await (
                PublicMessage(
                    title="🟢 Twinks Online",
                    color=discord.Color.green(),
                )
                .add_field(title="Guild", value=guild.name)
                .add_field(title="Latency", value=f"{round(self.latency * 1000)} ms")
                .channel(channel)
            )
        
        self.logger.info("----------------------------------------")
        self.logger.info("Twinks is now online!")
        self.logger.info("Logged in as %s", self.user)
        self.logger.info("User ID: %s", self.user.id)
        self.logger.info("Guilds: %d", len(self.guilds))
        self.logger.info("----------------------------------------")
        
    async def on_guild_join(self, guild: discord.Guild):
        await guild_setup.ensure(guild)
        self.logger.info("Configured %s", guild.name)


async def main():
    acquire()
    setup_logging(Config.LOG_PATH)
    bot = Twinks()
    try:
        async with bot:
            await bot.start(Config.BOT_TOKEN)
    finally:
        release()



if __name__ == "__main__":
    asyncio.run(main())