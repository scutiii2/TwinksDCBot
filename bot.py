from __future__ import annotations
import asyncio
import discord
from discord.ext import commands
from config import Config
import logging
from core.logging import setup_logging
from core.guild import guild_setup
from core.ui.message import PublicMessage
from cogs import COGS

class Twinks(commands.Bot):
    _cogs = {
        "moderation": True,
        "level_system": True,
        "game_manager": False
    }
    
    def __init__(self):
        self.logger = logging.getLogger("Twinks")
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            command_prefix="!",
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
        
        self.logger.info("Syncing application commands...")
        synced = await self.tree.sync()
        self.logger.info("Synced %d application commands.", len(synced))
        
        for guild in self.guilds:
            await guild_setup.ensure(guild)
            

    async def close(self):
        from core.database import database
        await database.close()
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
    setup_logging(Config.LOG_PATH)
    bot = Twinks()
    async with bot:
        await bot.start(Config.BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())