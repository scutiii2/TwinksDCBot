from __future__ import annotations

import discord


class Message:

    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        color: discord.Color = discord.Color.blurple(),
    ) -> None:

        self.embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )

    def add_field(
        self,
        value: str,
        title: str | None = None,
        inline: bool = False,
    ) -> "Message":

        self.embed.add_field(
            name=title or "\u200b",
            value=value,
            inline=inline,
        )

        return self


class EphemeralMessage(Message):
    async def send(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await interaction.response.send_message(
            embed=self.embed,
            ephemeral=True,
        )

    async def followup(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await interaction.followup.send(
            embed=self.embed,
            ephemeral=True,
        )


class PublicMessage(Message):
    async def send(
        self,
        interaction: discord.Interaction,
    ) -> None:

        await interaction.response.send_message(
            embed=self.embed,
        )

    async def followup(
        self,
        interaction: discord.Interaction,
    ) -> None:

        await interaction.followup.send(
            embed=self.embed,
        )

    async def channel(
        self,
        channel: discord.abc.Messageable,
    ) -> None:
        await channel.send(
            embed=self.embed,
        )
        
    async def send_to(
        self,
        destination: discord.abc.Messageable,
    ):
        await destination.send(embed=self.embed)