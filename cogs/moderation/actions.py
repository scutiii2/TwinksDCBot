from enum import StrEnum
from discord import Color

class ModerationAction(StrEnum):
    WARN = "warn"
    TIMEOUT = "timeout"
    KICK = "kick"
    BAN = "ban"
    UNBAN = "unban"
    SOFTBAN = "softban"
    NOTE = "note"
    UNTIMEOUT = "untimeout"
    
class ModerationActionIcon(StrEnum):
    WARN = "⚠️"
    TIMEOUT = "😶"
    KICK = "👟"
    BAN = "🔨"
    UNBAN = "🔧"
    SOFTBAN = "🪓"
    NOTE = "📝"
    UNTIMEOUT = "📢"

ModerationActionColor = {
    "WARN": Color.orange(),
    "TIMEOUT": Color.dark_grey(),
    "KICK": Color.red(),
    "BAN": Color.dark_red(),
    "UNBAN": Color.blue(),
    "SOFTBAN": Color.dark_orange(),
    "NOTE": Color.green(),
    "UNTIMEOUT": Color.light_grey(),
}