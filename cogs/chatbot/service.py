'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from core.database import databaseManager
from core.ollama import ollama_client
from config import Config
from .repository import ChatbotRepository as Repository

'''
===============================================================================
# &&Class ChatbotService
#   Provides utilities for Chatbot Cog
#   Middle man of the cog (talks to UI), the repository (whitelist),
#   and the OllamaClient (generation)
===============================================================================
'''
class ChatbotService:
# -----------------------------------------------------------------------------
# &&Method repository
#   Connector to the repository instance (global database)
# -----------------------------------------------------------------------------
    async def repository(self) -> Repository:
        db = await databaseManager.global_database(Repository.MIGRATIONS)
        return Repository(db)

# -----------------------------------------------------------------------------
# &&Method is_allowed
#   Checks whether a guild is whitelisted for the chatbot
# -----------------------------------------------------------------------------
    async def is_allowed(
        self,
        guild_id: int,
    ) -> bool:
        repo = await self.repository()
        return await repo.is_allowed(guild_id)

# -----------------------------------------------------------------------------
# &&Method add_guild
#   Whitelists a guild
# -----------------------------------------------------------------------------
    async def add_guild(
        self,
        guild_id: int,
        added_by: int,
    ) -> bool:
        repo = await self.repository()
        return await repo.add_guild(guild_id, added_by)

# -----------------------------------------------------------------------------
# &&Method remove_guild
#   Un-whitelists a guild
# -----------------------------------------------------------------------------
    async def remove_guild(
        self,
        guild_id: int,
    ) -> bool:
        repo = await self.repository()
        return await repo.remove_guild(guild_id)

# -----------------------------------------------------------------------------
# &&Method list_guilds
#   Returns every whitelisted guild
# -----------------------------------------------------------------------------
    async def list_guilds(self):
        repo = await self.repository()
        return await repo.list_guilds()

# -----------------------------------------------------------------------------
# &&Method ask
#   Sends a stateless prompt to Ollama and returns the generated text.
#   No conversation memory - every call is a fresh, independent prompt.
#   Always primed with the bot's persona via the system prompt.
# -----------------------------------------------------------------------------
    async def ask(
        self,
        prompt: str,
    ) -> str:
        return await ollama_client.generate(
            prompt,
            system=Config.OLLAMA_SYSTEM_PROMPT,
        )