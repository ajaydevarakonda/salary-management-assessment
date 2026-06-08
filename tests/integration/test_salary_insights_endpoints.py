import pytest

ENGINEER_INDIA = {
    "first_name": "Jane",
    "last_name": "Doe",
    "job_title": "Engineer",
    "department": "Engineering",
    "country": "India",
    "email": "jane.doe@example.com",
    "salary": "40000.00",
    "hire_date": "2022-01-15",
    "currency": "INR",
}

MANAGER_INDIA = {
    "first_name": "John",
    "last_name": "Smith",
    "job_title": "Manager",
    "department": "Engineering",
    "country": "India",
    "email": "john.smith@example.com",
    "salary": "80000.00",
    "hire_date": "2020-06-01",
    "currency": "INR",
}


@pytest.fixture
def seeded_client(client):
    """Provide a client with two employees already created."""
    assert client.post("/api/employees", json=ENGINEER_INDIA).status_code == 201
    assert client.post("/api/employees", json=MANAGER_INDIA).status_code == 201
    return client


class TestSalaryStatsByCountry:
    def test_returns_200_for_existing_country(self, seeded_client):
        response = seeded_client.get("/api/insights/salary-stats?country=India")
        print(seeded_client.app.routes)
        assert response.status_code == 200

    def test_returns_correct_minimum(self, seeded_client):
        response = seeded_client.get("/api/insights/salary-stats?country=India")
        assert response.json()[0]["minimum"] == "40000.00"

    def test_returns_correct_maximum(self, seeded_client):
        response = seeded_client.get("/api/insights/salary-stats?country=India")
        assert response.json()[0]["maximum"] == "80000.00"

    def test_returns_404_for_unknown_country(self, seeded_client):
        response = seeded_client.get("/api/insights/salary-stats?country=Mars")
        assert response.status_code == 404


class TestAverageSalaryByJobTitle:
    def test_returns_200_for_existing_country(self, seeded_client):
        response = seeded_client.get("/api/insights/salary-by-job-title?country=India")
        assert response.status_code == 200

    def test_returns_correct_job_titles(self, seeded_client):
        response = seeded_client.get("/api/insights/salary-by-job-title?country=India")
        job_titles = [item["job_title"] for item in response.json()]
        assert "Engineer" in job_titles
        assert "Manager" in job_titles

    def test_returns_404_for_unknown_country(self, seeded_client):
        response = seeded_client.get("/api/insights/salary-by-job-title?country=Mars")
        assert response.status_code == 404
