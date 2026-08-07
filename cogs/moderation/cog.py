'''
===============================================================================
# Search '&&Method' to see the start of every method
===============================================================================
'''

from __future__ import annotations
import discord
from discord import app_commands
from discord.ext import commands
from .service import ModerationService
from datetime import timedelta
from core.guild import guild_setup
from core.ui.message import PublicMessage, EphemeralMessage

'''
===============================================================================
# &&Class ModerationCog
#   For user types moderators
===============================================================================
'''
class ModerationCog(commands.Cog):

    def __init__(
        self,
        bot: commands.Bot,
    ):
        self.bot = bot
        self.service = ModerationService()

# -----------------------------------------------------------------------------
# &&Method warn
#   Add warning case to member
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="warn",
        description="Warn a member."
    )
    @app_commands.default_permissions(
        moderate_members=True,
    )
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
    ):

        case = await self.service.warn(
            guild_id=interaction.guild.id,
            target_id=member.id,
            moderator_id=interaction.user.id,
            reason=reason,
        )
        
        channel = await guild_setup.moderation_channel(
            interaction.guild
        )

        await (
            PublicMessage(
                title=f"[Case #{case}] ⚠ Warning Issued",
                color=discord.Color.orange(),
            )
            .add_field(
                title="Member",
                value=member.mention,
            )
            .add_field(
                title="Moderator",
                value=interaction.user.mention,
            )
            .add_field(
                title="Reason",
                value=reason or "No reason provided.",
            )
            .channel(channel)
        )
        
        await (
            EphemeralMessage(
                title=f"⚠ Warning Issued to {member.display_name}",
                color=discord.Color.orange(),
            )
            .send(interaction)
        )

# -----------------------------------------------------------------------------
# &&Method kick
#   Kick a member and record it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="kick",
        description="Kick a member."
    )
    @app_commands.default_permissions(
        kick_members=True,
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
    ):

        await member.kick(reason=reason)

        case = await self.service.kick(
            guild_id=interaction.guild.id,
            target_id=member.id,
            moderator_id=interaction.user.id,
            reason=reason,
        )

        await interaction.response.send_message(
            f"👢 Kicked {member.mention}\nCase #{case}"
        )

# -----------------------------------------------------------------------------
# &&Method ban
#   Ban a member and record it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="ban",
        description="Ban a member."
    )
    @app_commands.default_permissions(
        ban_members=True,
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
        delete_message_days: app_commands.Range[int, 0, 7] = 0,
    ):

        await member.ban(
            reason=reason,
            delete_message_days=delete_message_days,
        )

        case = await self.service.ban(
            guild_id=interaction.guild.id,
            target_id=member.id,
            moderator_id=interaction.user.id,
            reason=reason,
        )

        await interaction.response.send_message(
            f"🔨 Banned {member.mention}\nCase #{case}"
        )

# -----------------------------------------------------------------------------
# &&Method timeout
#   Give timeout to a member and record it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="timeout",
        description="Timeout a member."
    )
    @app_commands.default_permissions(
        moderate_members=True,
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        reason: str | None = None,
    ):

        duration = timedelta(minutes=minutes)

        await member.timeout(
            duration,
            reason=reason,
        )

        case = await self.service.timeout(
            guild_id=interaction.guild.id,
            target_id=member.id,
            moderator_id=interaction.user.id,
            duration=int(duration.total_seconds()),
            reason=reason,
        )

        await interaction.response.send_message(
            f"⏱️ Timed out {member.mention}\nCase #{case}"
        )

# -----------------------------------------------------------------------------
# &&Method note
#   Adds a note to a member and record it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="note",
        description="Add a moderation note."
    )
    @app_commands.default_permissions(
        moderate_members=True,
    )
    async def note(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        note: str,
    ):

        case = await self.service.note(
            guild_id=interaction.guild.id,
            target_id=member.id,
            moderator_id=interaction.user.id,
            note=note,
        )

        embed = discord.Embed(
            title=f"[Case #{case}] 📝Note: {member}",
            color=discord.Color.orange(),
        )

        embed.add_field(
            name=f"",
            value=note,
            inline=True,
        )
            
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )

# -----------------------------------------------------------------------------
# &&Method history
#   Checks the moderation history of a member
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="history",
        description="View a member's moderation history."
    )
    @app_commands.default_permissions(
        moderate_members=True,
    )
    async def history(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):

        cases = await self.service.history(
            guild_id=interaction.guild.id,
            target_id=member.id,
        )

        if not cases:

            await interaction.response.send_message(
                "No moderation history.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"{member} Moderation History",
            color=discord.Color.orange(),
        )

        for case in cases[:10]:

            embed.add_field(
                name=f"Case #{case['case_number']} • {case['action'].upper()}",
                value=case["reason"] or "No reason provided.",
                inline=False,
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )

# -----------------------------------------------------------------------------
# &&Method unban
#   Unban a member and records it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="unban",
        description="Unban a user."
    )
    @app_commands.default_permissions(
        ban_members=True,
    )
    async def unban(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        reason: str | None = None,
    ):

        await interaction.guild.unban(
            user,
            reason=reason,
        )

        case = await self.service.unban(
            guild_id=interaction.guild.id,
            moderator_id=interaction.user.id,
            target_id=user.id,
            reason=reason,
        )

        await interaction.response.send_message(
            f"✅ Unbanned {user.mention}\nCase #{case}"
        )

# -----------------------------------------------------------------------------
# &&Method untimeout
#   Untimeout a member and records it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="untimeout",
        description="Remove a timeout."
    )
    @app_commands.default_permissions(
        moderate_members=True,
    )
    async def untimeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
    ):

        await member.timeout(
            None,
            reason=reason,
        )

        case = await self.service.untimeout(
            guild_id=interaction.guild.id,
            moderator_id=interaction.user.id,
            target_id=member.id,
            reason=reason,
        )

        await interaction.response.send_message(
            f"✅ Timeout removed.\nCase #{case}"
        )

# -----------------------------------------------------------------------------
# &&Method purge
#   Purge latest the message/s of a member and records it
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="purge",
        description="Delete messages."
    )
    @app_commands.default_permissions(
        manage_messages=True,
    )
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100],
    ):

        await interaction.response.defer(
            ephemeral=True,
        )

        deleted = await interaction.channel.purge(
            limit=amount,
        )

        await interaction.followup.send(
            f"Deleted {len(deleted)} messages.",
            ephemeral=True,
        )

# -----------------------------------------------------------------------------
# &&Method clearwarnings
#   Clear any warnings given to the member
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="clearwarnings",
        description="Clear all warnings."
    )
    @app_commands.default_permissions(
        moderate_members=True,
    )
    async def clearwarnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):

        count = await self.service.clear_warnings(
            interaction.guild.id,
            member.id,
        )

        await interaction.response.send_message(
            f"Removed {count} warning(s)."
        )

# -----------------------------------------------------------------------------
# &&Method case
#   Check the history of any moderation case
# -----------------------------------------------------------------------------
    @app_commands.command(
        name="case",
        description="View a moderation case."
    )
    @app_commands.default_permissions(
        moderate_members=True,
    )
    async def case(
        self,
        interaction: discord.Interaction,
        case_number: int,
    ):

        case = await self.service.case(
            interaction.guild.id,
            case_number,
        )

        if case is None:

            await interaction.response.send_message(
                "Case not found.",
                ephemeral=True,
            )

            return

        embed = discord.Embed(
            title=f"Case #{case['case_number']}",
            color=discord.Color.blurple(),
        )

        embed.add_field(
            name="Action",
            value=case["action"],
        )

        embed.add_field(
            name="Target",
            value=f"<@{case['target_id']}>",
        )

        embed.add_field(
            name="Moderator",
            value=f"<@{case['moderator_id']}>",
        )

        embed.add_field(
            name="Status",
            value="Active" if case["active"] else "Closed",
            inline=False,
        )

        embed.add_field(
            name="Reason",
            value=case["reason"] or "No reason provided.",
            inline=False,
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )