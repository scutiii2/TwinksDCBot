from .setup import GuildSetupService
from .prefix import prefix_service

guild_setup = GuildSetupService()

__all__ = (
    "guild_setup",
    "prefix_service",
)