from .manager import DatabaseManager

database = DatabaseManager()

__all__ = (
    "database",
    "DatabaseManager",
)