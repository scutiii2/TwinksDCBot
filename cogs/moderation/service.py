from __future__ import annotations
from time import time
from core.database import database
from .actions import ModerationAction as ModAction, ModerationActionIcon as ModIcon, ModerationActionColor as ModColor
from .repository import ModerationRepository
from core.ui import PublicMessage, EphemeralMessage
from dataclasses import dataclass
from discord import Interaction, Member, User
from core.guild import guild_setup

@dataclass(slots=True)
class MessageField:
    title: str | None
    value: str

class ModerationService:
    async def create_message(
        self,
        case: int,
        service_type: ModAction,
        interaction: Interaction,
        member: Member | None = None,
        user: User | None = None,
        reason: str | None = None,
        note: str | None = None
    ) -> PublicMessage:
        channel = await guild_setup.moderation_channel(interaction.guild)
        message = (PublicMessage(
            title=f"[Case #{case}] {ModIcon[service_type.name]} {service_type.value.title()}",
            color=ModColor[service_type.name],
            )
            .add_field(
                title="Moderator",
                value=interaction.user.mention,
            )
        )
        
        if member:
            message.add_field(
                    title="Member",
                    value=member.mention,
                )
            
        if user:
            message.add_field(
                    title="User",
                    value=user,
                )
        
        if reason:
            message.add_field(
                    title="Reason",
                    value=reason,
                )
            
        if note:
            message.add_field(
                    title="Note",
                    value=note,
                )
            
        await message.channel(channel)
        
        await (
            EphemeralMessage(
                title=f"{ModIcon[service_type.name]} {service_type.value.title()} to {member.display_name}",
                color=ModColor[service_type.name],
            )
            .send(interaction)
        )

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
            action=ModAction.WARN,
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
            action=ModAction.TIMEOUT,
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
            action=ModAction.KICK,
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
            action=ModAction.BAN,
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
            action=ModAction.NOTE,
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
            action=ModAction.UNBAN,
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
            action=ModAction.UNTIMEOUT,
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
            ModAction.WARN,
        )


    async def case(
        self,
        guild_id: int,
        case_number: int,
    ):

        repo = await self.repository(guild_id)

        return await repo.get_case(case_number)