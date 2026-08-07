from __future__ import annotations
import discord

class GuildSetupService:
    CATEGORY_NAME = "🤖-Twinks"
    LOGS_CHANNEL = "📰-logs"
    MODERATION_CHANNEL = "👷-moderation"

    async def ensure(
        self,
        guild: discord.Guild,
    ) -> None:
        category = discord.utils.get(
            guild.categories,
            name=self.CATEGORY_NAME,
        )

        if category is None:
            category = await guild.create_category(
                self.CATEGORY_NAME
            )

        await self._ensure_logs(
            guild,
            category,
        )

        await self._ensure_moderation(
            guild,
            category,
        )

    async def _ensure_logs(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
    ):
        channel = discord.utils.get(
            category.text_channels,
            name=self.LOGS_CHANNEL,
        )

        if channel:
            return channel

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False,
            ),

            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
            ),
        }

        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=False,
                    read_message_history=True,
                )

        return await guild.create_text_channel(
            self.LOGS_CHANNEL,
            category=category,
            overwrites=overwrites,
        )
        
    async def _ensure_moderation(
        self,
        guild: discord.Guild,
        category: discord.CategoryChannel,
    ):

        channel = discord.utils.get(
            category.text_channels,
            name=self.MODERATION_CHANNEL,
        )

        if channel:
            return channel

        overwrites = {

            # Everyone
            guild.default_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True,
            ),

            # Twinks
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
            ),
        }

        # Allow administrators to send messages
        for role in guild.roles:

            if role.permissions.administrator:

                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                )

        return await guild.create_text_channel(
            self.MODERATION_CHANNEL,
            category=category,
            overwrites=overwrites,
        )
        
    async def logs_channel(
        self,
        guild: discord.Guild,
    ):
        await self.ensure(guild)
        category = discord.utils.get(
            guild.categories,
            name=self.CATEGORY_NAME,
        )

        return discord.utils.get(
            category.text_channels,
            name=self.LOGS_CHANNEL,
        )


    async def moderation_channel(
        self,
        guild: discord.Guild,
    ):
        await self.ensure(guild)
        category = discord.utils.get(
            guild.categories,
            name=self.CATEGORY_NAME,
        )

        return discord.utils.get(
            category.text_channels,
            name=self.MODERATION_CHANNEL,
        )