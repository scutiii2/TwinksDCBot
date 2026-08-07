from __future__ import annotations

from pathlib import Path
from typing import Any

import aiosqlite


class Database:
    """Represents a single SQLite database."""

    def __init__(self, path: Path):
        self._path = path
        self._connection: aiosqlite.Connection | None = None

    @property
    def path(self) -> Path:
        return self._path

    @property
    def is_connected(self) -> bool:
        return self._connection is not None

    async def connect(self) -> None:
        """Open the database connection."""
        if self._connection is not None:
            return

        self._path.parent.mkdir(parents=True, exist_ok=True)

        self._connection = await aiosqlite.connect(self._path)

        # Return rows like dictionaries
        self._connection.row_factory = aiosqlite.Row

        # Recommended SQLite settings
        await self._connection.execute("PRAGMA foreign_keys = ON;")
        await self._connection.execute("PRAGMA journal_mode = WAL;")
        await self._connection.execute("PRAGMA synchronous = NORMAL;")

        await self._connection.commit()

    async def close(self) -> None:
        """Close the database connection."""
        if self._connection is None:
            return

        await self._connection.close()
        self._connection = None

    async def execute(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> aiosqlite.Cursor:
        """Execute a query."""

        if self._connection is None:
            raise RuntimeError("Database is not connected.")

        cursor = await self._connection.execute(query, parameters)
        await self._connection.commit()
        return cursor

    async def executescript(self, script: str) -> None:
        """Execute multiple SQL statements."""

        if self._connection is None:
            raise RuntimeError("Database is not connected.")

        await self._connection.executescript(script)
        await self._connection.commit()

    async def fetchone(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> dict[str, Any] | None:
        """Fetch one row."""

        cursor = await self.execute(query, parameters)

        row = await cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    async def fetchall(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[dict[str, Any]]:
        """Fetch all rows."""

        cursor = await self.execute(query, parameters)

        rows = await cursor.fetchall()

        return [dict(row) for row in rows]