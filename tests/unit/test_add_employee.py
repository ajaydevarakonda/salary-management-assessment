import pytest
from decimal import Decimal
from datetime import date

from src.domain.employee import Employee
from src.use_cases.add_employee import AddEmployee
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
def add_employee(repository):
    return AddEmployee(repository)


class TestAddEmployee:
    def test_returns_employee_with_assigned_id(self, add_employee):
        employee = make_employee()
        result = add_employee.execute(employee)
        assert result.id is not None

    def test_persists_employee_to_repository(self, add_employee, repository):
        employee = make_employee()
        result = add_employee.execute(employee)
        assert repository.find_by_id(result.id) == result

    def test_preserves_employee_details(self, add_employee):
        employee = make_employee(first_name="John", last_name="Smith")
        result = add_employee.execute(employee)
        assert result.full_name() == "John Smith"
