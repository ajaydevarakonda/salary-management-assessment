import pytest
from decimal import Decimal
from datetime import date

from fastapi.testclient import TestClient

from src.domain.employee import Employee
from src.main import app
from src.api.dependencies import get_salary_insights_repository
from tests.unit.fake_salary_insights_repository import FakeSalaryInsightsRepository


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
def client():
    employees = [
        make_employee(country="India", job_title="Engineer", salary=Decimal("40000")),
        make_employee(country="India", job_title="Engineer", salary=Decimal("60000")),
        make_employee(country="India", job_title="Manager", salary=Decimal("80000")),
    ]
    repository = FakeSalaryInsightsRepository(employees)
    app.dependency_overrides[get_salary_insights_repository] = lambda: repository
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestSalaryStatsByCountry:
    def test_returns_200_with_stats(self, client):
        response = client.get("/insights/salary-stats?country=India")
        assert response.status_code == 200

    def test_returns_correct_min_max_average(self, client):
        response = client.get("/insights/salary-stats?country=India")
        data = response.json()[0]
        assert data["minimum"] == "40000"
        assert data["maximum"] == "80000"
        assert data["average"] == "60000"

    def test_returns_404_for_unknown_country(self, client):
        response = client.get("/insights/salary-stats?country=Mars")
        assert response.status_code == 404


class TestAverageSalaryByJobTitle:
    def test_returns_200_with_job_title_stats(self, client):
        response = client.get("/insights/salary-by-job-title?country=India")
        assert response.status_code == 200

    def test_returns_correct_job_titles(self, client):
        response = client.get("/insights/salary-by-job-title?country=India")
        job_titles = [item["job_title"] for item in response.json()]
        assert "Engineer" in job_titles
        assert "Manager" in job_titles

    def test_returns_404_for_unknown_country(self, client):
        response = client.get("/insights/salary-by-job-title?country=Mars")
        assert response.status_code == 404
