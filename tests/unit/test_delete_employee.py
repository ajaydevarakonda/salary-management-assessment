import pytest
from decimal import Decimal
from datetime import date

from src.domain.employee import Employee
from src.use_cases.add_employee import AddEmployee
from src.use_cases.delete_employee import DeleteEmployee
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
def delete_employee(repository):
    return DeleteEmployee(repository)


class TestDeleteEmployee:
    def test_removes_employee_from_repository(self, delete_employee, saved_employee, repository):
        delete_employee.execute(saved_employee.id)
        assert repository.find_by_id(saved_employee.id) is None

    def test_deleting_nonexistent_employee_does_not_raise(self, delete_employee):
        delete_employee.execute(999)
