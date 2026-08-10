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