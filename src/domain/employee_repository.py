from typing import Optional, Protocol

from src.domain.employee import Employee


class EmployeeRepository(Protocol):
    """Defines the contract for employee persistence."""

    def add(self, employee: Employee) -> Employee:
        """Persist a new employee and return it with its assigned id."""
        ...

    def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """Return the employee with the given id, or None if not found."""
        ...

    def find_all(self) -> list[Employee]:
        """Return all employees."""
        ...

    def update(self, employee: Employee) -> Employee:
        """Persist changes to an existing employee and return it."""
        ...

    def delete(self, employee_id: int) -> None:
        """Remove the employee with the given id."""
        ...
