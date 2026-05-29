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


class TestListEmployeesSearch:
    def test_search_by_first_name_returns_matching_employees(
        self, list_employees, add_employee
    ):
        alice = add_employee.execute(make_employee(first_name="Alice", email="alice@example.com"))
        add_employee.execute(make_employee(first_name="Bob", email="bob@example.com"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="alice")
        assert employees == [alice]
        assert total == 1

    def test_search_by_last_name_returns_matching_employees(
        self, list_employees, add_employee
    ):
        smith = add_employee.execute(make_employee(last_name="Smith", email="smith@example.com"))
        add_employee.execute(make_employee(last_name="Jones", email="jones@example.com"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="smith")
        assert employees == [smith]
        assert total == 1

    def test_search_by_email_returns_matching_employees(
        self, list_employees, add_employee
    ):
        target = add_employee.execute(make_employee(email="target@corp.com"))
        add_employee.execute(make_employee(email="other@corp.com"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="target")
        assert employees == [target]
        assert total == 1

    def test_search_by_country_returns_matching_employees(
        self, list_employees, add_employee
    ):
        add_employee.execute(make_employee(email="a@example.com", country="Brazil"))
        add_employee.execute(make_employee(email="b@example.com", country="India"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="brazil")
        assert len(employees) == 1
        assert total == 1

    def test_search_is_case_insensitive(self, list_employees, add_employee):
        alice = add_employee.execute(make_employee(first_name="Alice", email="alice@example.com"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="ALICE")
        assert employees == [alice]
        assert total == 1

    def test_search_total_reflects_filtered_count(self, list_employees, add_employee):
        for i in range(4):
            add_employee.execute(make_employee(first_name="Alice", email=f"alice{i}@example.com"))
        for i in range(3):
            add_employee.execute(make_employee(first_name="Bob", email=f"bob{i}@example.com"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="alice")
        assert len(employees) == 4
        assert total == 4

    def test_empty_search_returns_all_employees(self, list_employees, add_employee):
        add_employee.execute(make_employee(first_name="Alice", email="alice@example.com"))
        add_employee.execute(make_employee(first_name="Bob", email="bob@example.com"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="")
        assert len(employees) == 2
        assert total == 2

    def test_search_no_match_returns_empty_list_with_zero_total(
        self, list_employees, add_employee
    ):
        add_employee.execute(make_employee(first_name="Alice", email="alice@example.com"))
        employees, total = list_employees.execute_page(page=1, page_size=10, search="zzz")
        assert employees == []
        assert total == 0
