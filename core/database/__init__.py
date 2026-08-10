from .manager import DatabaseManager
from .database import Database

databaseManager = DatabaseManager()

__all__ = (
    "databaseManager",
    "Database",
    "DatabaseManager",
)