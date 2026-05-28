from passlib.context import CryptContext

from src.domain.user_repository import UserRepository
from src.infrastructure.jwt_service import create_access_token

_bcrypt_context = CryptContext(schemes=["bcrypt"])


class LoginUser:
    """Verifies user credentials and returns a JWT access token."""

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, username: str, password: str) -> str:
        """Return a JWT token if credentials are valid, otherwise raise."""
        user = self._repository.find_by_username(username)

        if not user or not _bcrypt_context.verify(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        return create_access_token(username)
