'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from pathlib import Path
from typing import Literal
from core.database.database import Database
from .actions import ModerationAction

'''
===============================================================================
# &&Class ModerationRepository
#   Talks to database
#   CASES SHOULD NOT BE DELETED AND SHOULD ONLY BE CLOSED
===============================================================================
'''
class ModerationRepository:
# -----------------------------------------------------------------------------
# &&Method constructor
#   Requirements to be detected by database manager
# -----------------------------------------------------------------------------
    MODULE = "moderation"
    MIGRATIONS = Path(__file__).parent / "migrations"
    def __init__(self, database: Database):
        self.db = database

# -----------------------------------------------------------------------------
# &&Method next_case_number
#   Database pointer of the repository
# -----------------------------------------------------------------------------
    async def next_case_number(self) -> int:
        row = await self.db.fetchone(
            """
            SELECT COALESCE(MAX(case_number), 0) + 1 AS number
            FROM cases
            """
        )
        return row["number"]

# -----------------------------------------------------------------------------
# &&Method create_case
#   Insert case into the database
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# &&Method get_case
#   Fetch a specific case from the database
# -----------------------------------------------------------------------------
    async def get_case(
        self,
        case_number: int
    ):
        return await self.db.fetchone(
            """
            SELECT *
            FROM cases
            WHERE case_number=?
            """,
            (case_number,),
        )

# -----------------------------------------------------------------------------
# &&Method get_cases
#   Fetch cases of a member and can be filtered by action
# -----------------------------------------------------------------------------
    async def get_cases(
        self,
        target_id: int,
        action: ModerationAction | None = None,
        active: Literal["True", "False", "All"] = "True"
    ):
        query = """
            SELECT *
            FROM cases
            WHERE target_id = ?
        """
        params = [target_id]
        if action:
            query += " AND action = ?"
            params.append(action.value)
        if active != "All":
            query += " AND active = ?"
            params.append([0, 1][active == "True"])
        query += " ORDER BY case_number DESC"
        return await self.db.fetchall(query, params)

# -----------------------------------------------------------------------------
# &&Method close_case
#   Closes a case
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# &&Method reopen_case
#   Reopens a case
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# &&Method clear_action
#   Sets the active records of a member in a specific action
# -----------------------------------------------------------------------------
    async def clear_action(
        self,
        target_id: int,
        action: ModerationAction,
    ) -> int:
        cursor = await self.db.execute(
            """
            UPDATE cases
            SET active=0
            WHERE target_id=?
            AND action=?
            """,
            (
                target_id,
                action.value,
            ),
        )
        return cursor.rowcount
    
# -----------------------------------------------------------------------------
# &&Method create_role_options
#   Create a role option message and its role mappings
# -----------------------------------------------------------------------------
    async def create_role_options(
        self,
        message_id: int,
        channel_id: int,
        roles: list[dict],
    ) -> None:
        await self.db.execute(
            """
            INSERT INTO role_options(
                message_id,
                channel_id
            )
            VALUES(
                ?, ?
            )
            """,
            (
                message_id,
                channel_id,
            ),
        )

        for role in roles:
            await self.db.execute(
                """
                INSERT INTO role_option_roles(
                    message_id,
                    role_id,
                    emoji
                )
                VALUES(
                    ?, ?, ?
                )
                """,
                (
                    message_id,
                    role["role_id"],
                    role["emoji"],
                ),
            )

# -----------------------------------------------------------------------------
# &&Method role_option
#   Fetch role option mappings for a message
# -----------------------------------------------------------------------------
    async def role_option(
        self,
        message_id: int,
    ):
        return await self.db.fetchall(
            """
            SELECT
                message_id,
                role_id,
                emoji
            FROM role_option_roles
            WHERE message_id=?
            ORDER BY rowid
            """,
            (
                message_id,
            ),
        )

# -----------------------------------------------------------------------------
# &&Method role_option_by_emoji
#   Fetch a role option using its message and emoji
# -----------------------------------------------------------------------------
    async def role_option_by_emoji(
        self,
        message_id: int,
        emoji: str,
    ):
        return await self.db.fetchone(
            """
            SELECT
                message_id,
                role_id,
                emoji
            FROM role_option_roles
            WHERE message_id=?
            AND emoji=?
            """,
            (
                message_id,
                emoji,
            ),
        )