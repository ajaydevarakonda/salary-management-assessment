import pytest
from decimal import Decimal
from datetime import date

from src.domain.employee import Employee
from src.use_cases.add_employee import AddEmployee
from src.use_cases.get_employee import GetEmployee
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
def get_employee(repository):
    return GetEmployee(repository)


@pytest.fixture
def saved_employee(repository):
    return AddEmployee(repository).execute(make_employee())


class TestGetEmployee:
    def test_returns_employee_by_id(self, get_employee, saved_employee):
        result = get_employee.execute(saved_employee.id)
        assert result == saved_employee

    def test_returns_none_when_employee_does_not_exist(self, get_employee):
        result = get_employee.execute(999)
        assert result is None
