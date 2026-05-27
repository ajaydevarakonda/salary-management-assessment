from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.domain.salary_stats import JobTitleSalaryStats


class GetAverageSalaryByJobTitle:
    """Retrieves average salary per job title for a given country."""

    def __init__(self, repository: SalaryInsightsRepository):
        self._repository = repository

    def execute(self, country: str) -> list[JobTitleSalaryStats]:
        """Return average salary and employee count per job title in a country."""
        return self._repository.get_average_salary_by_job_title(country)
