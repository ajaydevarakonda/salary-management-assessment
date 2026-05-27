from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository


class UpdateEmployee:
    """Persists changes to an existing employee."""

    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    def execute(self, employee: Employee) -> Employee:
        """Update the employee and return the updated state."""
        return self._repository.update(employee)
