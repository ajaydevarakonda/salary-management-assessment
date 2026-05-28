from typing import Optional

from dataclasses import replace

from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository


class FakeEmployeeRepository(EmployeeRepository):
    """In-memory employee repository for use in unit tests."""

    def __init__(self):
        self._store: dict[int, Employee] = {}
        self._next_id = 1

    def add(self, employee: Employee) -> Employee:
        """Persist employee with an auto-assigned id and return it."""
        employee_with_id = replace(employee, id=self._next_id)
        self._store[self._next_id] = employee_with_id
        self._next_id += 1
        return employee_with_id

    def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """Return the employee with the given id, or None if not found."""
        return self._store.get(employee_id)

    def find_all(self) -> list[Employee]:
        """Return all stored employees."""
        return list(self._store.values())

    def update(self, employee: Employee) -> Employee:
        """Overwrite the stored employee and return it."""
        self._store[employee.id] = employee
        return employee

    def delete(self, employee_id: int) -> None:
        """Remove the employee with the given id."""
        self._store.pop(employee_id, None)
