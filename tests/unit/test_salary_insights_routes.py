import pytest
from decimal import Decimal
from datetime import date

from fastapi.testclient import TestClient

from src.domain.currency_converter import CurrencyConverter
from src.domain.employee import Employee
from src.main import app
from src.api.dependencies import (
    get_currency_converter,
    get_current_user,
    get_salary_insights_repository,
)
from tests.unit.fake_salary_insights_repository import FakeSalaryInsightsRepository


class FakeCurrencyConverter:
    """Fake converter that returns amounts unchanged for route tests."""

    def to_usd(self, amount: Decimal, from_currency: str) -> Decimal:
        """Return amount as-is — routes tests care about shape, not conversion math."""
        return amount


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
def client():
    employees = [
        make_employee(country="India", job_title="Engineer", salary=Decimal("40000")),
        make_employee(country="India", job_title="Engineer", salary=Decimal("60000")),
        make_employee(country="India", job_title="Manager", salary=Decimal("80000")),
    ]
    repository = FakeSalaryInsightsRepository(employees)
    app.dependency_overrides[get_current_user] = lambda: "test_user"
    app.dependency_overrides[get_salary_insights_repository] = lambda: repository
    app.dependency_overrides[get_currency_converter] = lambda: FakeCurrencyConverter()
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestSalaryStatsByCountry:
    def test_returns_200_with_stats(self, client):
        response = client.get("/api/insights/salary-stats?country=India")
        assert response.status_code == 200

    def test_returns_correct_min_max_average(self, client):
        response = client.get("/api/insights/salary-stats?country=India")
        data = response.json()[0]
        assert data["minimum"] == "40000"
        assert data["maximum"] == "80000"
        assert data["average"] == "60000"

    def test_returns_currency_field(self, client):
        response = client.get("/api/insights/salary-stats?country=India")
        assert response.json()[0]["currency"] == "USD"

    def test_returns_404_for_unknown_country(self, client):
        response = client.get("/api/insights/salary-stats?country=Mars")
        assert response.status_code == 404


class TestAverageSalaryByJobTitle:
    def test_returns_200_with_job_title_stats(self, client):
        response = client.get("/api/insights/salary-by-job-title?country=India")
        assert response.status_code == 200

    def test_returns_correct_job_titles(self, client):
        response = client.get("/api/insights/salary-by-job-title?country=India")
        job_titles = [item["job_title"] for item in response.json()]
        assert "Engineer" in job_titles
        assert "Manager" in job_titles

    def test_returns_currency_field(self, client):
        response = client.get("/api/insights/salary-by-job-title?country=India")
        assert all(item["currency"] == "USD" for item in response.json())

    def test_returns_404_for_unknown_country(self, client):
        response = client.get("/api/insights/salary-by-job-title?country=Mars")
        assert response.status_code == 404
