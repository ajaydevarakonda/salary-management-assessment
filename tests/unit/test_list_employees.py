import pytest
from decimal import Decimal
from datetime import date

from src.domain.employee import Employee
from src.use_cases.add_employee import AddEmployee
from src.use_cases.list_employees import ListEmployees
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
def list_employees(repository):
    return ListEmployees(repository)


@pytest.fixture
def add_employee(repository):
    return AddEmployee(repository)


class TestListEmployees:
    def test_returns_empty_list_when_no_employees_exist(self, list_employees):
        assert list_employees.execute() == []

    def test_returns_all_added_employees(self, list_employees, add_employee):
        first = add_employee.execute(make_employee(first_name="Jane"))
        second = add_employee.execute(make_employee(first_name="John"))
        assert list_employees.execute() == [first, second]

    def test_returns_correct_employee_count(self, list_employees, add_employee):
        add_employee.execute(make_employee(first_name="Jane"))
        add_employee.execute(make_employee(first_name="John"))
        assert len(list_employees.execute()) == 2


class TestListEmployeesPaginated:
    def test_returns_items_and_total(self, list_employees, add_employee):
        add_employee.execute(make_employee(first_name="Jane"))
        add_employee.execute(make_employee(first_name="John"))
        employees, total = list_employees.execute_page(page=1, page_size=10)
        assert len(employees) == 2
        assert total == 2

    def test_returns_correct_page(self, list_employees, add_employee):
        for i in range(5):
            add_employee.execute(make_employee(first_name=f"User{i}", email=f"user{i}@example.com"))
        employees, total = list_employees.execute_page(page=1, page_size=3)
        assert len(employees) == 3
        assert total == 5

    def test_second_page_returns_remaining_items(self, list_employees, add_employee):
        for i in range(5):
            add_employee.execute(make_employee(first_name=f"User{i}", email=f"user{i}@example.com"))
        employees, total = list_employees.execute_page(page=2, page_size=3)
        assert len(employees) == 2
        assert total == 5

    def test_empty_page_returns_empty_list_with_zero_total(self, list_employees):
        employees, total = list_employees.execute_page(page=1, page_size=10)
        assert employees == []
        assert total == 0
