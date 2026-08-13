'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from pathlib import Path
from time import time
from core.database import Database

'''
===============================================================================
# &&Class ChatbotRepository
#   Talks to database
#   Lives in the GLOBAL database (bot-wide whitelist, not per-guild)
===============================================================================
'''
class ChatbotRepository:
# -----------------------------------------------------------------------------
# &&Method constructor
#   Requirements to be detected by database manager
# -----------------------------------------------------------------------------
    MIGRATIONS = Path(__file__).parent / "migrations"
    def __init__(self, database: Database):
        self.db = database

# -----------------------------------------------------------------------------
# &&Method add_guild
#   Whitelist a guild. Returns True if newly added, False if already present.
# -----------------------------------------------------------------------------
    async def add_guild(
        self,
        guild_id: int,
        added_by: int,
    ) -> bool:
        cursor = await self.db.execute(
            """
            INSERT OR IGNORE INTO allowed_guilds(guild_id, added_by, added_at)
            VALUES(?, ?, ?)
            """,
            (guild_id, added_by, int(time())),
        )
        return cursor.rowcount > 0

# -----------------------------------------------------------------------------
# &&Method remove_guild
#   Un-whitelist a guild. Returns True if a row was removed.
# -----------------------------------------------------------------------------
    async def remove_guild(
        self,
        guild_id: int,
    ) -> bool:
        cursor = await self.db.execute(
            """
            DELETE FROM allowed_guilds
            WHERE guild_id = ?
            """,
            (guild_id,),
        )
        return cursor.rowcount > 0

# -----------------------------------------------------------------------------
# &&Method is_allowed
#   Check if a guild_id exists in allowed_guilds
# -----------------------------------------------------------------------------
    async def is_allowed(
        self,
        guild_id: int,
    ) -> bool:
        row = await self.db.fetchone(
            """
            SELECT 1
            FROM allowed_guilds
            WHERE guild_id = ?
            """,
            (guild_id,),
        )
        return row is not None

# -----------------------------------------------------------------------------
# &&Method list_guilds
#   Fetch every whitelisted guild
# -----------------------------------------------------------------------------
    async def list_guilds(self):
        return await self.db.fetchall(
            """
            SELECT *
            FROM allowed_guilds
            ORDER BY added_at DESC
            """
        )
