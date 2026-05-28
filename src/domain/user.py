from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents an admin user of the system."""

    username: str
    hashed_password: str
    id: Optional[int] = None
