from src.domain.employee_repository import EmployeeRepository
from src.domain.salary_insights_repository import SalaryInsightsRepository


def get_employee_repository() -> EmployeeRepository:
    """Provide the employee repository instance."""
    raise NotImplementedError("Wire a real repository in main.py")


def get_salary_insights_repository() -> SalaryInsightsRepository:
    """Provide the salary insights repository instance."""
    raise NotImplementedError("Wire a real repository in main.py")
