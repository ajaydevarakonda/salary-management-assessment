import pytest
from dataclasses import replace
from decimal import Decimal
from datetime import date

from src.domain.employee import Employee
from src.use_cases.add_employee import AddEmployee
from src.use_cases.update_employee import UpdateEmployee
from tests.unit.fake_employee_repository import FakeEmployeeRepository


def make_employee(**overrides) -> Employee:
    """Return a valid Employee with optional field overrides."""
    defaults = {
        "first_name": "Jane",
        "last_name": "Doe",
        "job_title": "Engineer",
        "department": "Engineering",
        "country": "India",
        "email": "jane.doe@example.com",
        "salary": Decimal("50000.00"),
        "hire_date": date(2022, 1, 15),
    }
    return Employee(**{**defaults, **overrides})


@pytest.fixture
def repository():
    return FakeEmployeeRepository()


@pytest.fixture
def saved_employee(repository):
    return AddEmployee(repository).execute(make_employee())


@pytest.fixture
def update_employee(repository):
    return UpdateEmployee(repository)


class TestUpdateEmployee:
    def test_returns_updated_employee(self, update_employee, saved_employee):
        updated = replace(saved_employee, job_title="Senior Engineer")
        result = update_employee.execute(updated)
        assert result.job_title == "Senior Engineer"

    def test_persists_updated_employee(self, update_employee, saved_employee, repository):
        updated = replace(saved_employee, salary=Decimal("75000.00"))
        update_employee.execute(updated)
        assert repository.find_by_id(saved_employee.id).salary == Decimal("75000.00")
