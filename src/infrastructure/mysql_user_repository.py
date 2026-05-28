from typing import Optional

from sqlalchemy.orm import Session

from src.domain.user import User
from src.domain.user_repository import UserRepository
from src.infrastructure.models.user_model import UserModel


class MysqlUserRepository(UserRepository):
    """SQLAlchemy implementation of the UserRepository protocol."""

    def __init__(self, session: Session):
        self._session = session

    def find_by_username(self, username: str) -> Optional[User]:
        """Return the user with the given username, or None if not found."""
        model = (
            self._session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )
        if not model:
            return None
        return User(
            id=model.id,
            username=model.username,
            hashed_password=model.hashed_password,
        )
