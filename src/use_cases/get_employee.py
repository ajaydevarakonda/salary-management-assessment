from typing import Optional

from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository


class GetEmployee:
    """Retrieves a single employee by id."""

    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    def execute(self, employee_id: int) -> Optional[Employee]:
        """Return the employee with the given id, or None if not found."""
        return self._repository.find_by_id(employee_id)
