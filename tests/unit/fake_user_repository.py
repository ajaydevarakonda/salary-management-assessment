from typing import Optional

from src.domain.user import User
from src.domain.user_repository import UserRepository


class FakeUserRepository(UserRepository):
    """In-memory user repository for use in unit tests."""

    def __init__(self, users: list[User] = None):
        self._store: dict[str, User] = {
            user.username: user for user in (users or [])
        }

    def find_by_username(self, username: str) -> Optional[User]:
        """Return the user with the given username, or None if not found."""
        return self._store.get(username)
