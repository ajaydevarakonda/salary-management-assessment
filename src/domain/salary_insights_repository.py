from typing import Protocol

from src.domain.salary_stats import JobTitleSalaryStats, SalaryStats


class SalaryInsightsRepository(Protocol):
    """Defines the contract for salary aggregation queries."""

    def get_salary_stats_by_country(self, country: str) -> list[SalaryStats]:
        """Return min, max, average salary and employee count for a country."""
        ...

    def get_average_salary_by_job_title(
        self, country: str
    ) -> list[JobTitleSalaryStats]:
        """Return average salary per job title, optionally filtered by country."""
        ...
