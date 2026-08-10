from __future__ import annotations
from pathlib import Path
from core.database import databaseManager

DEFAULT_PREFIX = "!"


class PrefixService:
    MIGRATIONS = Path(__file__).parent / "migrations"

    def __init__(self):
        self._cache: dict[int, str] = {}

    async def _db(self):
        return await databaseManager.global_database(self.MIGRATIONS)

    async def get(self, guild_id: int) -> str:
        if guild_id in self._cache:
            return self._cache[guild_id]

        db = await self._db()
        row = await db.fetchone(
            "SELECT prefix FROM guild_prefixes WHERE guild_id = ?",
            (guild_id,),
        )
        prefix = row["prefix"] if row else DEFAULT_PREFIX
        self._cache[guild_id] = prefix
        return prefix

    async def set(self, guild_id: int, prefix: str) -> None:
        db = await self._db()
        await db.execute(
            """
            INSERT INTO guild_prefixes(guild_id, prefix)
            VALUES(?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET prefix = excluded.prefix
            """,
            (guild_id, prefix),
        )
        self._cache[guild_id] = prefix


prefix_service = PrefixService()