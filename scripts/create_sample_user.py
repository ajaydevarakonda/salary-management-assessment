"""Create a sample user from credentials defined in .env."""

import os

from dotenv import load_dotenv

from src.infrastructure.database import SessionLocal
from src.infrastructure.models.user_model import UserModel
from src.use_cases.login_user import _bcrypt_context

load_dotenv()

USERNAME = os.getenv("SAPMLE_USERNAME")
PASSWORD = os.getenv("SAMPLE_PASSWORD")


def create_sample_user() -> None:
    """Insert the sample user into the database if they don't already exist."""
    session = SessionLocal()
    try:
        exists = session.query(UserModel).filter_by(username=USERNAME).first()
        if exists:
            print(f"User '{USERNAME}' already exists.")
            return
        session.add(UserModel(username=USERNAME, hashed_password=_bcrypt_context.hash(PASSWORD)))
        session.commit()
        print(f"User '{USERNAME}' created.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    create_sample_user()
