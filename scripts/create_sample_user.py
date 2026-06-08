"""Create a sample user from credentials defined in .env."""

import os

import bcrypt
from dotenv import load_dotenv

from src.infrastructure.database import SessionLocal
from src.infrastructure.models.user_model import UserModel

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
        hashed = bcrypt.hashpw(PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        session.add(UserModel(username=USERNAME, hashed_password=hashed))
        session.commit()
        print(f"User '{USERNAME}' created.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    create_sample_user()
