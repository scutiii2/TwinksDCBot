from __future__ import annotations
from time import time
from core.database import database
from .actions import ModerationAction
from .repository import ModerationRepository
from core.ui import EphemeralMessage
from discord import Color
from dataclasses import dataclass

@dataclass(slots=True)
class MessageField:
    title: str | None
    value: str

class ModerationService:
    async def create_message(
        self,
        case: int,
        member_name: str,
        service_type: ModerationAction,
        color: Color = Color.blurple(),
        fields: list[MessageField] | None = None,
    ) -> EphemeralMessage:
        message = EphemeralMessage(
            title=f"[Case #{case}] {service_type.value.title()} - {member_name}",
            color=color,
        )

        if fields:
            for field in fields:

                message.add_field(
                    title=field.title,
                    value=field.value,
                )

        return message

    async def repository(
        self,
        guild_id: int,
    ) -> ModerationRepository:

        db = await database.guild_module(
            guild_id,
            ModerationRepository.MODULE,
            ModerationRepository.MIGRATIONS,
        )

        return ModerationRepository(db)

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

    async def history(
        self,
        guild_id: int,
        target_id: int,
    ):

        repo = await self.repository(guild_id)

        return await repo.get_cases(target_id)
    
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


    async def clear_warnings(
        self,
        guild_id: int,
        target_id: int,
    ) -> int:

        repo = await self.repository(guild_id)

        return await repo.clear_action(
            target_id,
            ModerationAction.WARN,
        )


    async def case(
        self,
        guild_id: int,
        case_number: int,
    ):

        repo = await self.repository(guild_id)

        return await repo.get_case(case_number)