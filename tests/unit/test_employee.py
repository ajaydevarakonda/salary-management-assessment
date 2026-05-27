import pytest
from decimal import Decimal
from datetime import date

from src.domain.employee import Employee


def make_valid_employee(**overrides) -> Employee:
    """Return a valid Employee, with optional field overrides."""
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


class TestFullName:
    def test_combines_first_and_last_name(self):
        employee = make_valid_employee(first_name="Jane", last_name="Doe")
        assert employee.full_name() == "Jane Doe"


class TestSalaryValidation:
    def test_raises_when_salary_is_zero(self):
        with pytest.raises(ValueError, match="Salary must be positive"):
            make_valid_employee(salary=Decimal("0"))

    def test_raises_when_salary_is_negative(self):
        with pytest.raises(ValueError, match="Salary must be positive"):
            make_valid_employee(salary=Decimal("-1000"))


class TestNameValidation:
    def test_raises_when_first_name_is_empty(self):
        with pytest.raises(ValueError, match="First name cannot be empty"):
            make_valid_employee(first_name="")

    def test_raises_when_last_name_is_empty(self):
        with pytest.raises(ValueError, match="Last name cannot be empty"):
            make_valid_employee(last_name="")
