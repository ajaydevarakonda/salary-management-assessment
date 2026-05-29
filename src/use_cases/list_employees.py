from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository


class ListEmployees:
    """Retrieves all employees."""

    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    def execute(self) -> list[Employee]:
        """Return all employees."""
        return self._repository.find_all()

    def execute_page(
        self, page: int, page_size: int
    ) -> tuple[list[Employee], int]:
        """Return one page of employees and the total count."""
        employees = self._repository.find_page(page, page_size)
        total = self._repository.count()
        return employees, total
