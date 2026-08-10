'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from core.database import databaseManager
from .repository import LevelSystemRepository as Repository
from .leveling import level_from_xp

'''
===============================================================================
# &&Class LevelSystemService
#   Provides utilities for Level System Cog (and other cogs, e.g. game_manager)
#   Middle man of the cog (talks to UI) and repository (talks to databaseManager)
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
        db = await databaseManager.guild_module(
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
# &&Method is_registered
#   Checks whether a member is registered
# -----------------------------------------------------------------------------
    async def is_registered(
        self,
        user_id: int,
        guild_id: int,
    ) -> bool:
        repo = await self.repository(guild_id)
        return await repo.check_user(user_id, guild_id)

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
# &&Method add_xp
#   Awards XP to a member (auto-registers if needed).
#   Public entry point for OTHER cogs (e.g. game_manager) to grant XP.
#   Returns (old_level, new_level) so callers can detect level-ups.
# -----------------------------------------------------------------------------
    async def add_xp(
        self,
        user_id: int,
        guild_id: int,
        amount: int,
    ) -> tuple[int, int]:
        repo = await self.repository(guild_id)
        before = await repo.get_user(user_id, guild_id)
        old_level = before["level"] if before else 0
        row = await repo.add_xp(user_id, guild_id, amount)
        new_level = level_from_xp(row["xp"])
        if new_level != old_level:
            await repo.set_level(user_id, guild_id, new_level)
        return old_level, new_level

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
        
