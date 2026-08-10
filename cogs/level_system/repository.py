'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from pathlib import Path
from core.database import Database

'''
===============================================================================
# &&Class LevelSystemRepository
#   Talks to database
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
        cursor = await self.db.execute(
            """
            INSERT OR IGNORE INTO user_levels(user_id, guild_id)
            VALUES(?, ?)
            """,
            (user_id, guild_id),
        )
        return cursor.rowcount > 0
    
# -----------------------------------------------------------------------------
# &&Method check_user
#   Check if a user_id exists in user_levels
# -----------------------------------------------------------------------------
    async def check_user(
        self,
        user_id: int,
        guild_id: int
    ) -> bool:
        row = await self.db.fetchone(
            """
            SELECT 1
            FROM user_levels
            WHERE user_id = ? AND guild_id = ?
            """,
            (user_id, guild_id),
        )
        return row is not None

# -----------------------------------------------------------------------------
# &&Method get_user
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
# &&Method add_xp
#   Adds XP to a user, auto-registering them if needed. Returns updated row.
# -----------------------------------------------------------------------------
    async def add_xp(
        self,
        user_id: int,
        guild_id: int,
        amount: int,
    ) -> dict:
        await self.db.execute(
            """
            INSERT INTO user_levels(user_id, guild_id, xp)
            VALUES(?, ?, ?)
            ON CONFLICT(user_id, guild_id)
            DO UPDATE SET xp = xp + excluded.xp
            """,
            (user_id, guild_id, amount),
        )
        return await self.get_user(user_id, guild_id)

# -----------------------------------------------------------------------------
# &&Method set_level
#   Updates the cached level column after an XP change
# -----------------------------------------------------------------------------
    async def set_level(
        self,
        user_id: int,
        guild_id: int,
        level: int,
    ) -> None:
        await self.db.execute(
            """
            UPDATE user_levels
            SET level = ?
            WHERE user_id = ? AND guild_id = ?
            """,
            (level, user_id, guild_id),
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