from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    STORAGE_PATH = Path("storage")
    LOG_PATH = Path("logs")
    DEBUG = False
    DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")

    # --- Crafty Controller ---
    CRAFTY_BASE_URL = os.getenv("CRAFTY_BASE_URL")
    CRAFTY_API_TOKEN = os.getenv("CRAFTY_API_TOKEN")
    CRAFTY_SERVER_ID = os.getenv("CRAFTY_SERVER_ID")
    CRAFTY_VERIFY_SSL = os.getenv("CRAFTY_VERIFY_SSL", "false").lower() == "true"