from __future__ import annotations
from pathlib import Path
from .database import Database

class MigrationManager:
    """Applies SQL migrations to a database."""

    TABLE_NAME = "__migrations"

    def __init__(self, database: Database):
        self._database = database

    async def migrate(self, directory: Path) -> None:
        """Apply all pending migrations in a directory."""

        if not directory.exists():
            return

        await self._create_migration_table()

        applied = await self._get_applied_migrations()

        migration_files = sorted(directory.glob("*.sql"))

        for migration in migration_files:

            migration_id = migration.stem

            if migration_id in applied:
                continue

            sql = migration.read_text(encoding="utf-8")

            await self._database.executescript(sql)

            await self._database.execute(
                f"""
                INSERT INTO {self.TABLE_NAME}(id)
                VALUES(?)
                """,
                (migration_id,),
            )

    async def _create_migration_table(self) -> None:
        await self._database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id TEXT PRIMARY KEY,
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    async def _get_applied_migrations(self) -> set[str]:

        rows = await self._database.fetchall(
            f"""
            SELECT id
            FROM {self.TABLE_NAME}
            """
        )

        return {row["id"] for row in rows}