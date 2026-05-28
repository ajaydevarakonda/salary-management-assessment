from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.domain.employee_repository import EmployeeRepository
from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.infrastructure.database import get_session
from src.infrastructure.jwt_service import decode_access_token
from src.domain.user_repository import UserRepository
from src.infrastructure.mysql_employee_repository import MysqlEmployeeRepository
from src.infrastructure.mysql_salary_insights_repository import MysqlSalaryInsightsRepository
from src.infrastructure.mysql_user_repository import MysqlUserRepository

_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    """Decode the JWT token and return the username, or raise 401."""
    try:
        return decode_access_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


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


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    """Provide a MySQL-backed user repository."""
    return MysqlUserRepository(session)
