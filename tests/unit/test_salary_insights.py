import pytest
from decimal import Decimal
from datetime import date

from src.domain.currency_converter import CurrencyConverter
from src.domain.employee import Employee
from src.use_cases.get_salary_stats_by_country import GetSalaryStatsByCountry
from src.use_cases.get_average_salary_by_job_title import GetAverageSalaryByJobTitle
from tests.unit.fake_salary_insights_repository import FakeSalaryInsightsRepository


class FakeCurrencyConverter:
    """Fake converter using fixed rates for unit tests."""

    _RATES = {
        "USD": Decimal("1"),
        "INR": Decimal("0.012"),
        "GBP": Decimal("1.27"),
    }

    def to_usd(self, amount: Decimal, from_currency: str) -> Decimal:
        """Convert amount to USD using fixed test rates."""
        if from_currency not in self._RATES:
            raise ValueError(f"Unsupported currency: {from_currency}")
        return (amount * self._RATES[from_currency]).quantize(Decimal("0.01"))


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
        "currency": "USD",
    }
    return Employee(**{**defaults, **overrides})


@pytest.fixture
def converter():
    return FakeCurrencyConverter()


@pytest.fixture
def employees():
    return [
        make_employee(country="India", job_title="Engineer", salary=Decimal("40000")),
        make_employee(country="India", job_title="Engineer", salary=Decimal("60000")),
        make_employee(country="India", job_title="Manager", salary=Decimal("80000")),
        make_employee(country="USA", job_title="Engineer", salary=Decimal("100000")),
    ]


@pytest.fixture
def repository(employees):
    return FakeSalaryInsightsRepository(employees)


class TestGetSalaryStatsByCountry:
    def test_calculates_minimum_salary(self, repository, converter):
        result = GetSalaryStatsByCountry(repository, converter).execute("India")
        assert result[0].minimum == Decimal("40000.00")

    def test_calculates_maximum_salary(self, repository, converter):
        result = GetSalaryStatsByCountry(repository, converter).execute("India")
        assert result[0].maximum == Decimal("80000.00")

    def test_calculates_average_salary(self, repository, converter):
        result = GetSalaryStatsByCountry(repository, converter).execute("India")
        assert result[0].average == Decimal("60000.00")

    def test_returns_correct_employee_count(self, repository, converter):
        result = GetSalaryStatsByCountry(repository, converter).execute("India")
        assert result[0].employee_count == 3

    def test_returns_empty_list_for_unknown_country(self, repository, converter):
        result = GetSalaryStatsByCountry(repository, converter).execute("Mars")
        assert result == []

    def test_result_currency_is_usd(self, repository, converter):
        result = GetSalaryStatsByCountry(repository, converter).execute("India")
        assert result[0].currency == "USD"

    def test_converts_inr_salaries_to_usd(self, converter):
        employees = [
            make_employee(country="India", salary=Decimal("40000"), currency="INR"),
            make_employee(
                country="India",
                salary=Decimal("60000"),
                currency="INR",
                email="other@example.com",
            ),
        ]
        repository = FakeSalaryInsightsRepository(employees)
        result = GetSalaryStatsByCountry(repository, converter).execute("India")
        assert result[0].minimum == Decimal("480.00")
        assert result[0].maximum == Decimal("720.00")
        assert result[0].currency == "USD"


class TestGetAverageSalaryByJobTitle:
    def test_returns_stats_for_each_job_title_in_country(self, repository, converter):
        result = GetAverageSalaryByJobTitle(repository, converter).execute("India")
        job_titles = [s.job_title for s in result]
        assert "Engineer" in job_titles
        assert "Manager" in job_titles

    def test_calculates_average_salary_per_job_title(self, repository, converter):
        result = GetAverageSalaryByJobTitle(repository, converter).execute("India")
        engineer = next(s for s in result if s.job_title == "Engineer")
        assert engineer.average == Decimal("50000.00")

    def test_excludes_employees_from_other_countries(self, repository, converter):
        result = GetAverageSalaryByJobTitle(repository, converter).execute("India")
        assert len(result) == 2

    def test_returns_correct_employee_count_per_job_title(self, repository, converter):
        result = GetAverageSalaryByJobTitle(repository, converter).execute("India")
        engineer = next(s for s in result if s.job_title == "Engineer")
        assert engineer.employee_count == 2

    def test_result_currency_is_usd(self, repository, converter):
        result = GetAverageSalaryByJobTitle(repository, converter).execute("India")
        assert all(s.currency == "USD" for s in result)

    def test_converts_inr_salaries_to_usd(self, converter):
        employees = [
            make_employee(
                country="India",
                job_title="Engineer",
                salary=Decimal("100000"),
                currency="INR",
            ),
            make_employee(
                country="India",
                job_title="Engineer",
                salary=Decimal("100000"),
                currency="INR",
                email="other@example.com",
            ),
        ]
        repository = FakeSalaryInsightsRepository(employees)
        result = GetAverageSalaryByJobTitle(repository, converter).execute("India")
        engineer = next(s for s in result if s.job_title == "Engineer")
        assert engineer.average == Decimal("1200.00")
        assert engineer.currency == "USD"
