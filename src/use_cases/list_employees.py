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
        self, page: int, page_size: int, search: str = ""
    ) -> tuple[list[Employee], int]:
        """Return one page of employees and the total count, optionally filtered."""
        employees = self._repository.find_page(page, page_size, search)
        total = self._repository.count(search)
        return employees, total
