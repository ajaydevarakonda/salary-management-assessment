from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.domain.salary_stats import JobTitleSalaryStats, SalaryStats
from src.infrastructure.models.employee_model import EmployeeModel


class MysqlSalaryInsightsRepository(SalaryInsightsRepository):
    """SQLAlchemy implementation of the SalaryInsightsRepository protocol."""

    def __init__(self, session: Session):
        self._session = session

    def get_salary_stats_by_country(self, country: str) -> list[SalaryStats]:
        """Return min, max, average salary and employee count for a country."""
        result = (
            self._session.query(
                func.min(EmployeeModel.salary),
                func.max(EmployeeModel.salary),
                func.avg(EmployeeModel.salary),
                func.count(EmployeeModel.id),
            )
            .filter(EmployeeModel.country == country)
            .one()
        )

        minimum, maximum, average, count = result
        if count == 0:
            return []

        return [
            SalaryStats(
                country=country,
                minimum=Decimal(str(minimum)),
                maximum=Decimal(str(maximum)),
                average=Decimal(str(average)),
                employee_count=count,
            )
        ]

    def get_average_salary_by_job_title(
        self, country: str
    ) -> list[JobTitleSalaryStats]:
        """Return average salary and employee count per job title in a country."""
        rows = (
            self._session.query(
                EmployeeModel.job_title,
                func.avg(EmployeeModel.salary),
                func.count(EmployeeModel.id),
            )
            .filter(EmployeeModel.country == country)
            .group_by(EmployeeModel.job_title)
            .order_by(func.avg(EmployeeModel.salary).desc())
            .all()
        )

        return [
            JobTitleSalaryStats(
                job_title=job_title,
                average=Decimal(str(average)),
                employee_count=count,
            )
            for job_title, average, count in rows
        ]
