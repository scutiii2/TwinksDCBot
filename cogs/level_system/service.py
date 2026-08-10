'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from core.database import database
from .repository import LevelSystemRepository as Repository

'''
===============================================================================
# &&Class LevelSystemService
#   Provides utilities for Level System Cog
#   Middle man of the cog (talks to UI) and repository (talks to database)
===============================================================================
'''
class LevelSystemService:
# -----------------------------------------------------------------------------
# &&Method repository
#   Connector the the repository instance of the guild
# -----------------------------------------------------------------------------
    async def repository(
        self,
        guild_id: int,
    ) -> Repository:
        db = await database.guild_module(
            guild_id,
            Repository.MODULE,
            Repository.MIGRATIONS,
        )
        return Repository(db)

# -----------------------------------------------------------------------------
# &&Method register
#   Creates user level info for a member
# -----------------------------------------------------------------------------
    async def register(
        self,
        user_id: int,
        guild_id: int,
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.create_user(user_id, guild_id)

# -----------------------------------------------------------------------------
# &&Method get_user
#   Returns level info
# -----------------------------------------------------------------------------
    async def get_user(
        self,
        user_id: int,
        guild_id: int,
    ) -> dict | None:
        repo = await self.repository(guild_id)
        return await repo.get_user(user_id, guild_id)

# -----------------------------------------------------------------------------
# &&Method get_top_users
#   Get top N users
# -----------------------------------------------------------------------------
    async def get_top_users(
        self,
        guild_id: int,
        overall: bool = False,
        count: int = 10
    ) -> list:
        repo = await self.repository(guild_id)
        if overall:
            return await repo.get_top_users(count)
        else:
            return await repo.get_guild_top_users(guild_id, count)
        
