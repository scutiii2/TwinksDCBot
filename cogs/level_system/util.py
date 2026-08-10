from discord import Interaction, Member, User
from core.guild import guild_setup
from core.ui import PublicMessage, EphemeralMessage


# -----------------------------------------------------------------------------
# &&Method create_message
#   Direct messenger to the guild after doing moderation commands
# -----------------------------------------------------------------------------
# async def create_message(
#     case: int,
#     interaction: Interaction,
# ) -> PublicMessage:
#     channel = await guild_setup.moderation_channel(interaction.guild)
#     message = (PublicMessage(
#         title=f"[Case #{case}] {ModerationActionIcon[service_type.name]} {service_type.value.title()}",
#         color=ModerationActionColor[service_type.name],
#         )
#         .add_field(
#             title="Moderator",
#             value=interaction.user.mention,
#         )
#     )
    
#     fields = [
#         ("Member", member.mention if member else None),
#         ("User", user),
#         ("Reason", reason),
#         ("Note", note),
#     ]
#     for title, value in fields:
#         if value:
#             message.add_field(title=title, value=value)

#     await message.channel(channel)
#     await (
#         EphemeralMessage(
#             title=f"{ModerationActionIcon[service_type.name]} {service_type.value.title()} to {member.display_name}",
#             color=ModerationActionColor[service_type.name],
#         )
#         .send(interaction)
#     )