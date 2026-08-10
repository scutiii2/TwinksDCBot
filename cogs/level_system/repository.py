'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from pathlib import Path
from core.database.database import Database

'''
===============================================================================
# &&Class LevelSystemRepository
#   Talks to database
#   CASES SHOULD NOT BE DELETED AND SHOULD ONLY BE CLOSED
===============================================================================
'''
class LevelSystemRepository:
# -----------------------------------------------------------------------------
# &&Method constructor
#   Requirements to be detected by database manager
# -----------------------------------------------------------------------------
    MODULE = "level_system"
    MIGRATIONS = Path(__file__).parent / "migrations"
    def __init__(self, database: Database):
        self.db = database

# -----------------------------------------------------------------------------
# &&Method create_user
#   Insert case into the database
# -----------------------------------------------------------------------------
    async def create_user(
        self,
        user_id: int,
        guild_id: int
    ) -> int:
        await self.db.execute(
            """
            INSERT INTO user_levels(
                user_id,
                guild_id
            )
            VALUES(
                ?, ?
            )
            """,
            (
                user_id,
                guild_id,
            ),
        )
        return user_id
    
# -----------------------------------------------------------------------------
# &&Method check_user
#   Check if a user_id exists in user_levels
# -----------------------------------------------------------------------------
    async def check_user(
        self,
        user_id: int,
        guild_id: int
    ) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1
                FROM user_levels
                WHERE user_id = ? AND guild_id = ?
            )
        """
        result = await self.db.fetchone(query, (user_id, guild_id))
        return bool(result[0])

# -----------------------------------------------------------------------------
# &&Method get_case
#   Fetch a specific case from the database
# -----------------------------------------------------------------------------
    async def get_user(
        self,
        user_id: int,
        guild_id: int
    ):
        return await self.db.fetchone(
            """
            SELECT *
            FROM user_levels
            WHERE user_id=?
            AND guild_id=?
            """,
            (user_id, guild_id),
        )

# -----------------------------------------------------------------------------
# &&Method get_guild_top_users
#   Fetch top N users in a guild
# -----------------------------------------------------------------------------
    async def get_guild_top_users(
        self,
        guild_id: int,
        count: int = 10
    ):
        limit = count if count > 0 else 10
        query = """
            SELECT user_id, xp, level
            FROM user_levels
            WHERE guild_id = ?
            ORDER BY xp DESC
            LIMIT ?
        """
        return await self.db.fetchall(query, (guild_id, limit))

# -----------------------------------------------------------------------------
# &&Method get_top_users
#   Fetch overall top N users (global leaderboard)
# -----------------------------------------------------------------------------
    async def get_top_users(
        self,
        count: int = 10
    ):
        limit = count if count > 0 else 10
        query = """
            SELECT user_id, xp, level
            FROM user_levels
            ORDER BY xp DESC
            LIMIT ?
        """
        return await self.db.fetchall(query, (limit))