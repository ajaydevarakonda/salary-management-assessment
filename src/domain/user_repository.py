from typing import Optional, Protocol

from src.domain.user import User


class UserRepository(Protocol):
    """Defines the contract for user persistence."""

    def find_by_username(self, username: str) -> Optional[User]:
        """Return the user with the given username, or None if not found."""
        ...
