from .user_info import UserInfo
from .decorator import is_bot_owner

user_info = UserInfo()

__all__ = (
    "user_info",
    "is_bot_owner",
)