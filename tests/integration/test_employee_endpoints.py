import pytest

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


class TestCreateEmployee:
    def test_creates_employee_and_returns_201(self, client):
        response = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD)
        assert response.status_code == 201

    def test_created_employee_has_assigned_id(self, client):
        response = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD)
        assert response.json()["id"] is not None

    def test_created_employee_has_correct_details(self, client):
        response = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD)
        data = response.json()
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Doe"
        assert data["job_title"] == "Engineer"


class TestGetEmployee:
    def test_returns_employee_by_id(self, client):
        created = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        response = client.get(f"/employees/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_returns_404_for_nonexistent_employee(self, client):
        response = client.get("/employees/99999")
        assert response.status_code == 404


class TestListEmployees:
    def test_returns_empty_list_initially(self, client):
        response = client.get("/employees")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_all_created_employees(self, client):
        client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD)
        client.post("/employees", json={
            **VALID_EMPLOYEE_PAYLOAD,
            "first_name": "John",
            "email": "john.doe@example.com",
        })
        response = client.get("/employees")
        assert len(response.json()) == 2


class TestUpdateEmployee:
    def test_updates_employee_details(self, client):
        created = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        updated_payload = {**VALID_EMPLOYEE_PAYLOAD, "job_title": "Senior Engineer"}
        response = client.put(f"/employees/{created['id']}", json=updated_payload)
        assert response.status_code == 200
        assert response.json()["job_title"] == "Senior Engineer"

    def test_persists_update_to_database(self, client):
        created = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        updated_payload = {**VALID_EMPLOYEE_PAYLOAD, "job_title": "Senior Engineer"}
        client.put(f"/employees/{created['id']}", json=updated_payload)
        response = client.get(f"/employees/{created['id']}")
        assert response.json()["job_title"] == "Senior Engineer"


class TestDeleteEmployee:
    def test_deletes_employee_and_returns_204(self, client):
        created = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        response = client.delete(f"/employees/{created['id']}")
        assert response.status_code == 204

    def test_employee_not_found_after_deletion(self, client):
        created = client.post("/employees", json=VALID_EMPLOYEE_PAYLOAD).json()
        client.delete(f"/employees/{created['id']}")
        response = client.get(f"/employees/{created['id']}")
        assert response.status_code == 404
