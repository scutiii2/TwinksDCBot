'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
from time import time
from typing import Literal
from core.database import database
from .actions import ModerationAction
from .repository import ModerationRepository as Repository

'''
===============================================================================
# &&Class ModerationService
#   Provides utilities for Moderation Cog
#   Middle man of the cog (talks to UI) and repository (talks to database)
===============================================================================
'''
class ModerationService:
# -----------------------------------------------------------------------------
# &&Method repository
#   Connector the the repository instance of the guild
# -----------------------------------------------------------------------------
    async def repository(
        self,
        guild_id: int,
    ) -> Repository:
        db = await database.guild_module(
            guild_id,
            Repository.MODULE,
            Repository.MIGRATIONS,
        )
        return Repository(db)

# -----------------------------------------------------------------------------
# &&Method warn
#   Create a WARN case against a member
# -----------------------------------------------------------------------------
    async def warn(
        self,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        reason: str | None,
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.create_case(
            target_id=target_id,
            moderator_id=moderator_id,
            action=ModerationAction.WARN,
            reason=reason,
            created_at=int(time()),
        )

# -----------------------------------------------------------------------------
# &&Method kick
#   Create a KICK case against a member
# -----------------------------------------------------------------------------
    async def kick(
        self,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        reason: str | None,
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.create_case(
            target_id=target_id,
            moderator_id=moderator_id,
            action=ModerationAction.KICK,
            reason=reason,
            created_at=int(time()),
        )

# -----------------------------------------------------------------------------
# &&Method timeout
#   Create a TIMEOUT case against a member
# -----------------------------------------------------------------------------
    async def timeout(
        self,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        duration: int,
        reason: str | None,
    ) -> int:
        repo = await self.repository(guild_id)
        now = int(time())
        return await repo.create_case(
            target_id=target_id,
            moderator_id=moderator_id,
            action=ModerationAction.TIMEOUT,
            reason=reason,
            created_at=now,
            expires_at=now + duration,
        )

# -----------------------------------------------------------------------------
# &&Method untimeout
#   Create a UNTIMEOUT case against a member
# -----------------------------------------------------------------------------
    async def untimeout(
        self,
        guild_id: int,
        moderator_id: int,
        target_id: int,
        reason: str | None,
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.create_case(
            target_id=target_id,
            moderator_id=moderator_id,
            action=ModerationAction.UNTIMEOUT,
            reason=reason,
            created_at=int(time()),
        )

# -----------------------------------------------------------------------------
# &&Method ban
#   Create a BAN case against a member
# -----------------------------------------------------------------------------
    async def ban(
        self,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        reason: str | None,
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.create_case(
            target_id=target_id,
            moderator_id=moderator_id,
            action=ModerationAction.BAN,
            reason=reason,
            created_at=int(time()),
        )

# -----------------------------------------------------------------------------
# &&Method unban
#   Create a UNBAN case against a member
# -----------------------------------------------------------------------------
    async def unban(
        self,
        guild_id: int,
        moderator_id: int,
        target_id: int,
        reason: str | None,
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.create_case(
            target_id=target_id,
            moderator_id=moderator_id,
            action=ModerationAction.UNBAN,
            reason=reason,
            created_at=int(time()),
        )

# -----------------------------------------------------------------------------
# &&Method note
#   Create a NOTE case against a member
# -----------------------------------------------------------------------------
    async def note(
        self,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        note: str,
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.create_case(
            target_id=target_id,
            moderator_id=moderator_id,
            action=ModerationAction.NOTE,
            reason=note,
            created_at=int(time()),
        )

# -----------------------------------------------------------------------------
# &&Method clear_warnings
#   Delete all warnings on a member
# -----------------------------------------------------------------------------
    async def clear_action(
        self,
        guild_id: int,
        target_id: int,
        action: ModerationAction
    ) -> int:
        repo = await self.repository(guild_id)
        return await repo.clear_action(
            target_id,
            action
        )

# -----------------------------------------------------------------------------
# &&Method case
#   Shows specific case by number
# -----------------------------------------------------------------------------
    async def case(
        self,
        guild_id: int,
        case_number: int,
    ):
        repo = await self.repository(guild_id)
        return await repo.get_case(case_number)

# -----------------------------------------------------------------------------
# &&Method history
#   Shows all cases of a member and can be filtered by action
# -----------------------------------------------------------------------------
    async def history(
        self,
        guild_id: int,
        target_id: int,
        action: ModerationAction | None = None,
        active: Literal["True", "False", "All"] = "True"
    ):
        repo = await self.repository(guild_id)
        return await repo.get_cases(target_id, action, active)
