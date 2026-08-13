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
        migrations: Path | None = None,
    ) -> Database:
        path = self._storage / "global.db"
        return await self._open(path, migrations)

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

        # Reuse the connection if this file is already open, but ALWAYS run
        # migrations below regardless of cache state. Multiple modules can
        # share the same database file (e.g. global.db is used by both
        # prefix_service and chatbot) - each with its own migrations
        # directory. If we skip migrate() on a cache hit, whichever module
        # opens the file first "wins" and every other module's tables never
        # get created. MigrationManager.migrate() is idempotent (it tracks
        # applied migration IDs itself), so calling it on every _open() is
        # safe and cheap - it's a no-op once a given migration file has
        # already been applied.
        if path in self._databases:
            database = self._databases[path]
        else:
            database = Database(path)
            await database.connect()
            self._databases[path] = database

        if migrations is not None:
            manager = MigrationManager(database)
            await manager.migrate(migrations)

        return database

    async def close(self) -> None:

        for database in self._databases.values():

            await database.close()

        self._databases.clear()