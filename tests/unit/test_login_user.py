import pytest
from passlib.context import CryptContext

from src.domain.user import User
from src.use_cases.login_user import LoginUser
from tests.unit.fake_user_repository import FakeUserRepository

bcrypt_context = CryptContext(schemes=["bcrypt"])


def make_user(username: str = "admin", password: str = "secret") -> User:
    """Return a User with a bcrypt-hashed password."""
    return User(
        username=username,
        hashed_password=bcrypt_context.hash(password),
    )


@pytest.fixture
def repository():
    return FakeUserRepository(users=[make_user()])


@pytest.fixture
def login_user(repository):
    return LoginUser(repository)


class TestLoginUser:
    def test_returns_token_for_valid_credentials(self, login_user):
        token = login_user.execute("admin", "secret")
        assert token is not None

    def test_raises_for_wrong_password(self, login_user):
        with pytest.raises(ValueError, match="Invalid credentials"):
            login_user.execute("admin", "wrongpassword")

    def test_raises_for_unknown_username(self, login_user):
        with pytest.raises(ValueError, match="Invalid credentials"):
            login_user.execute("unknown", "secret")
