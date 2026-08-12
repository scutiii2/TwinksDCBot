from .client import CraftyClient, CraftyError

crafty_client = CraftyClient()

__all__ = (
    "crafty_client",
    "CraftyError",
)