import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api.dependencies import get_current_user
from src.infrastructure.database import Base, get_session
from src.infrastructure.models.employee_model import EmployeeModel  # noqa: F401
from src.main import app

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest.fixture(scope="session")
def engine():
    """Create the test database schema once for the whole test session."""
    test_engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(test_engine)
    yield test_engine
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def session(engine):
    """Provide a transactional session that rolls back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    test_session = sessionmaker(bind=connection)()
    yield test_session
    test_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(session):
    """Provide a TestClient wired to the transactional test session."""
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_current_user] = lambda: "test_user"
    yield TestClient(app)
    app.dependency_overrides.clear()
