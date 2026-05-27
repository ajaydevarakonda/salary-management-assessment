from sqlalchemy.orm import Session
from fastapi import Depends

from src.domain.employee_repository import EmployeeRepository
from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.infrastructure.database import get_session
from src.infrastructure.mysql_employee_repository import MysqlEmployeeRepository
from src.infrastructure.mysql_salary_insights_repository import MysqlSalaryInsightsRepository


def get_employee_repository(
    session: Session = Depends(get_session),
) -> EmployeeRepository:
    """Provide a MySQL-backed employee repository."""
    return MysqlEmployeeRepository(session)


def get_salary_insights_repository(
    session: Session = Depends(get_session),
) -> SalaryInsightsRepository:
    """Provide a MySQL-backed salary insights repository."""
    return MysqlSalaryInsightsRepository(session)
