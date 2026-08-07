from __future__ import annotations

from pathlib import Path

from core.database.database import Database

from .actions import ModerationAction


class ModerationRepository:

    MODULE = "moderation"

    MIGRATIONS = Path(__file__).parent / "migrations"

    def __init__(
        self,
        database: Database,
    ):
        self.db = database

    async def next_case_number(self) -> int:

        row = await self.db.fetchone(
            """
            SELECT COALESCE(MAX(case_number), 0) + 1 AS number
            FROM cases
            """
        )

        return row["number"]

    async def create_case(
        self,
        target_id: int,
        moderator_id: int,
        action: ModerationAction,
        reason: str | None,
        created_at: int,
        expires_at: int | None = None,
    ) -> int:

        case_number = await self.next_case_number()

        await self.db.execute(
            """
            INSERT INTO cases(
                case_number,
                target_id,
                moderator_id,
                action,
                reason,
                created_at,
                expires_at
            )
            VALUES(
                ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                case_number,
                target_id,
                moderator_id,
                action.value,
                reason,
                created_at,
                expires_at,
            ),
        )

        return case_number

    async def get_case(
        self,
        case_number: int,
    ):

        return await self.db.fetchone(
            """
            SELECT *
            FROM cases
            WHERE case_number=?
            """,
            (case_number,),
        )

    async def get_cases(
        self,
        target_id: int,
    ):

        return await self.db.fetchall(
            """
            SELECT *
            FROM cases
            WHERE target_id=?
            ORDER BY case_number DESC
            """,
            (target_id,),
        )

    async def close_case(
        self,
        case_number: int,
    ):

        await self.db.execute(
            """
            UPDATE cases
            SET active=0
            WHERE case_number=?
            """,
            (case_number,),
        )
            
    async def reopen_case(
        self,
        case_number: int,
    ) -> None:

        await self.db.execute(
            """
            UPDATE cases
            SET active = 1
            WHERE case_number = ?
            """,
            (case_number,),
        )


    async def clear_action(
        self,
        target_id: int,
        action: ModerationAction,
    ) -> int:

        cursor = await self.db.execute(
            """
            DELETE FROM cases
            WHERE target_id = ?
            AND action = ?
            """,
            (
                target_id,
                action.value,
            ),
        )

        return cursor.rowcount


    async def delete_case(
        self,
        case_number: int,
    ) -> bool:

        cursor = await self.db.execute(
            """
            DELETE FROM cases
            WHERE case_number = ?
            """,
            (case_number,),
        )

        return cursor.rowcount > 0