import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.api.dependencies import get_current_user, get_employee_repository
from tests.unit.fake_employee_repository import FakeEmployeeRepository


VALID_EMPLOYEE_PAYLOAD = {
    "first_name": "Jane",
    "last_name": "Doe",
    "job_title": "Engineer",
    "department": "Engineering",
    "country": "India",
    "email": "jane.doe@example.com",
    "salary": "50000.00",
    "hire_date": "2022-01-15",
}


@pytest.fixture
def client():
    repository = FakeEmployeeRepository()
    app.dependency_overrides[get_current_user] = lambda: "test_user"
    app.dependency_overrides[get_employee_repository] = lambda: repository
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestCreateEmployee:
    def test_returns_201_with_assigned_id(self, client):
        response = client.post("/api/employees", json=VALID_EMPLOYEE_PAYLOAD)
        assert response.status_code == 201
        assert response.json()["id"] is not None

    def test_returns_created_employee_details(self, client):
        response = client.post("/api/employees", json=VALID_EMPLOYEE_PAYLOAD)
        assert response.json()["first_name"] == "Jane"
        assert response.json()["last_name"] == "Doe"


class TestGetEmployee:
    def test_returns_200_with_employee(self, client):
        created = client.post("/api/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        response = client.get(f"/api/employees/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_returns_404_when_employee_not_found(self, client):
        response = client.get("/api/employees/999")
        assert response.status_code == 404


class TestListEmployees:
    def test_returns_200_with_empty_list(self, client):
        response = client.get("/api/employees")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_all_employees(self, client):
        client.post("/api/employees", json=VALID_EMPLOYEE_PAYLOAD)
        client.post("/api/employees", json={**VALID_EMPLOYEE_PAYLOAD, "first_name": "John"})
        response = client.get("/api/employees")
        assert len(response.json()) == 2


class TestUpdateEmployee:
    def test_returns_200_with_updated_employee(self, client):
        created = client.post("/api/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        updated_payload = {**VALID_EMPLOYEE_PAYLOAD, "job_title": "Senior Engineer"}
        response = client.put(f"/api/employees/{created['id']}", json=updated_payload)
        assert response.status_code == 200
        assert response.json()["job_title"] == "Senior Engineer"

    def test_returns_404_when_employee_not_found(self, client):
        response = client.put("/api/employees/999", json=VALID_EMPLOYEE_PAYLOAD)
        assert response.status_code == 404


class TestDeleteEmployee:
    def test_returns_204_on_success(self, client):
        created = client.post("/api/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        response = client.delete(f"/api/employees/{created['id']}")
        assert response.status_code == 204

    def test_employee_no_longer_exists_after_deletion(self, client):
        created = client.post("/api/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        client.delete(f"/api/employees/{created['id']}")
        response = client.get(f"/api/employees/{created['id']}")
        assert response.status_code == 404
