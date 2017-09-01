from enum import Enum

class Roles(Enum):
    """User roles that affect available commands."""
    OWNER = 0
    MOD = 1
    BANNED = 2
