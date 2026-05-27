from src.domain.employee_repository import EmployeeRepository


class DeleteEmployee:
    """Removes an employee from the repository."""

    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    def execute(self, employee_id: int) -> None:
        """Delete the employee with the given id."""
        self._repository.delete(employee_id)
