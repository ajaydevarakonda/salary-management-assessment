from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.domain.salary_stats import SalaryStats


class GetSalaryStatsByCountry:
    """Retrieves salary statistics grouped by country."""

    def __init__(self, repository: SalaryInsightsRepository):
        self._repository = repository

    def execute(self, country: str) -> list[SalaryStats]:
        """Return min, max, average salary and employee count for a country."""
        return self._repository.get_salary_stats_by_country(country)
