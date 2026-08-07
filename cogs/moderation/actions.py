from enum import StrEnum


class ModerationAction(StrEnum):
    WARN = "warn"
    TIMEOUT = "timeout"
    KICK = "kick"
    BAN = "ban"
    UNBAN = "unban"
    SOFTBAN = "softban"
    NOTE = "note"
    UNTIMEOUT = "untimeout"