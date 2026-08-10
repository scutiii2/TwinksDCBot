from __future__ import annotations
import discord


async def safe_defer(
    interaction: discord.Interaction,
    ephemeral: bool = False,
) -> None:
    """Defer the interaction if nothing has responded yet.

    Call this as the very first line of any check or command that does
    I/O (DB calls, HTTP requests, Discord API lookups) before it knows
    what to reply with. Guards against the 3-second ack window expiring
    and prevents 'interaction already acknowledged' errors from double-
    deferring.
    """
    if interaction.response.is_done():
        return
    try:
        await interaction.response.defer(ephemeral=ephemeral)
    except discord.NotFound:
        pass  # interaction already expired; nothing more we can do