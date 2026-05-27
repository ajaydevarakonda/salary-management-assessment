from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository


class ListEmployees:
    """Retrieves all employees."""

    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    def execute(self) -> list[Employee]:
        """Return all employees."""
        return self._repository.find_all()
