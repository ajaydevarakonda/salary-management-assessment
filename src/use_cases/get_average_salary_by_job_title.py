from src.domain.currency_converter import CurrencyConverter
from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.domain.salary_stats import JobTitleSalaryStats


class GetAverageSalaryByJobTitle:
    """Retrieves average salary per job title for a given country, converted to USD."""

    def __init__(
        self,
        repository: SalaryInsightsRepository,
        converter: CurrencyConverter,
    ):
        self._repository = repository
        self._converter = converter

    def execute(self, country: str) -> list[JobTitleSalaryStats]:
        """Return average salary and employee count per job title in a country in USD."""
        stats = self._repository.get_average_salary_by_job_title(country)
        return [
            JobTitleSalaryStats(
                job_title=s.job_title,
                average=self._converter.to_usd(s.average, s.currency),
                employee_count=s.employee_count,
                currency="USD",
            )
            for s in stats
        ]
