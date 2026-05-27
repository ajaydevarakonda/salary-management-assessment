from decimal import Decimal

from src.domain.employee import Employee
from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.domain.salary_stats import JobTitleSalaryStats, SalaryStats


class FakeSalaryInsightsRepository(SalaryInsightsRepository):
    """In-memory salary insights repository for use in unit tests."""

    def __init__(self, employees: list[Employee]):
        self._employees = employees

    def get_salary_stats_by_country(self, country: str) -> list[SalaryStats]:
        """Compute salary stats for the given country."""
        salaries = [
            e.salary for e in self._employees if e.country == country
        ]
        if not salaries:
            return []
        return [
            SalaryStats(
                country=country,
                minimum=min(salaries),
                maximum=max(salaries),
                average=sum(salaries) / len(salaries),
                employee_count=len(salaries),
            )
        ]

    def get_average_salary_by_job_title(
        self, country: str
    ) -> list[JobTitleSalaryStats]:
        """Compute average salary per job title for the given country."""
        job_titles: dict[str, list[Decimal]] = {}
        for employee in self._employees:
            if employee.country == country:
                job_titles.setdefault(employee.job_title, []).append(
                    employee.salary
                )

        return [
            JobTitleSalaryStats(
                job_title=job_title,
                average=sum(salaries) / len(salaries),
                employee_count=len(salaries),
            )
            for job_title, salaries in job_titles.items()
        ]
