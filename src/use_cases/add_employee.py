from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository


class AddEmployee:
    """Persists a new employee to the repository."""

    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    def execute(self, employee: Employee) -> Employee:
        """Add the employee and return it with its assigned id."""
        return self._repository.add(employee)
