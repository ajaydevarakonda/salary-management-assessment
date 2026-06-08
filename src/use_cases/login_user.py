import bcrypt

from src.domain.user_repository import UserRepository
from src.infrastructure.jwt_service import create_access_token


class LoginUser:
    """Verifies user credentials and returns a JWT access token."""

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, username: str, password: str) -> str:
        """Return a JWT token if credentials are valid, otherwise raise."""
        user = self._repository.find_by_username(username)

        password_matches = user and bcrypt.checkpw(
            password.encode("utf-8"),
            user.hashed_password.encode("utf-8"),
        )
        if not password_matches:
            raise ValueError("Invalid credentials")
        return create_access_token(username)
