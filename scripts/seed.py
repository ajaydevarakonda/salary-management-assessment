"""Seed the database with 10,000 employee records."""

import pathlib
import random
import time
from datetime import date

from faker import Faker
from sqlalchemy import insert

from src.infrastructure.database import SessionLocal
from src.infrastructure.models.employee_model import EmployeeModel

DATA_DIR = pathlib.Path(__file__).parent / "data"


def _load_names() -> tuple[list[str], list[str]]:
    """Load first and last name lists from scripts/data/."""
    first_names = (DATA_DIR / "first_names.txt").read_text().splitlines()
    last_names = (DATA_DIR / "last_names.txt").read_text().splitlines()
    return first_names, last_names

RECORD_COUNT = 10_000
BATCH_SIZE = 1_000

DEPARTMENTS = [
    "Engineering",
    "Marketing",
    "Sales",
    "Finance",
    "Human Resources",
    "Operations",
    "Product",
    "Legal",
    "Customer Support",
    "Research & Development",
]

JOB_TITLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Product Manager",
    "Data Analyst",
    "Marketing Specialist",
    "Sales Representative",
    "Financial Analyst",
    "HR Manager",
    "Operations Manager",
    "UX Designer",
    "DevOps Engineer",
    "QA Engineer",
    "Business Analyst",
    "Account Manager",
    "Legal Counsel",
]

COUNTRIES = [
    "India",
    "United States",
    "United Kingdom",
    "Germany",
    "Canada",
    "Australia",
    "Singapore",
    "Netherlands",
    "France",
    "Brazil",
]


def build_records(count: int) -> list[dict]:
    """Generate a list of employee record dicts."""
    fake = Faker()
    first_names, last_names = _load_names()
    records = []
    for index in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        records.append(
            {
                "first_name": first_name,
                "last_name": last_name,
                "job_title": random.choice(JOB_TITLES),
                "department": random.choice(DEPARTMENTS),
                "country": random.choice(COUNTRIES),
                "email": f"{first_name.lower()}.{last_name.lower()}.{index}@example.com",
                "salary": round(random.uniform(30_000, 200_000), 2),
                "hire_date": fake.date_between(
                    start_date=date(2010, 1, 1), end_date=date(2024, 12, 31)
                ),
            }
        )
    return records


def seed(count: int = RECORD_COUNT) -> None:
    """Insert employee records into the database in batches."""
    print(f"Generating {count:,} records...")
    gen_start = time.perf_counter()
    records = build_records(count)
    gen_elapsed = time.perf_counter() - gen_start
    print(f"Generated in {gen_elapsed:.2f}s. Inserting in batches of {BATCH_SIZE:,}...")

    session = SessionLocal()
    try:
        insert_start = time.perf_counter()
        for batch_start in range(0, count, BATCH_SIZE):
            batch = records[batch_start : batch_start + BATCH_SIZE]
            session.execute(insert(EmployeeModel), batch)
            session.commit()
            print(f"  Inserted {min(batch_start + BATCH_SIZE, count):,}/{count:,}")
        insert_elapsed = time.perf_counter() - insert_start
        print(f"Done. Inserted {count:,} records in {insert_elapsed:.2f}s.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
