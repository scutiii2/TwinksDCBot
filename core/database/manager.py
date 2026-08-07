from __future__ import annotations

from pathlib import Path

from .database import Database
from .migration import MigrationManager


class DatabaseManager:

    def __init__(
        self,
        storage_path: Path = Path("storage"),
    ) -> None:

        self._storage = storage_path

        self._databases: dict[Path, Database] = {}

    async def global_database(
        self,
    ) -> Database:

        path = self._storage / "global.db"

        return await self._open(path)

    async def user_database(
        self,
        user_id: int,
        migrations: Path | None = None,
    ) -> Database:

        path = self._storage / "users" / f"{user_id}.db"

        return await self._open(
            path,
            migrations,
        )

    async def guild_module(
        self,
        guild_id: int,
        module: str,
        migrations: Path | None = None,
    ) -> Database:

        path = (
            self._storage
            / "guilds"
            / str(guild_id)
            / f"{module}.db"
        )

        return await self._open(
            path,
            migrations,
        )

    async def _open(
        self,
        path: Path,
        migrations: Path | None = None,
    ) -> Database:

        if path in self._databases:

            return self._databases[path]

        database = Database(path)

        await database.connect()

        if migrations is not None:

            manager = MigrationManager(database)

            await manager.migrate(migrations)

        self._databases[path] = database

        return database

    async def close(self) -> None:

        for database in self._databases.values():

            await database.close()

        self._databases.clear()