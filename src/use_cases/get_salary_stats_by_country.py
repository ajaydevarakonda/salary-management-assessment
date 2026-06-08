from src.domain.currency_converter import CurrencyConverter
from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.domain.salary_stats import SalaryStats


class GetSalaryStatsByCountry:
    """Retrieves salary statistics grouped by country, converted to USD."""

    def __init__(
        self,
        repository: SalaryInsightsRepository,
        converter: CurrencyConverter,
    ):
        self._repository = repository
        self._converter = converter

    def execute(self, country: str) -> list[SalaryStats]:
        """Return min, max, average salary and employee count for a country in USD."""
        stats = self._repository.get_salary_stats_by_country(country)
        return [
            SalaryStats(
                country=s.country,
                minimum=self._converter.to_usd(s.minimum, s.currency),
                maximum=self._converter.to_usd(s.maximum, s.currency),
                average=self._converter.to_usd(s.average, s.currency),
                employee_count=s.employee_count,
                currency="USD",
            )
            for s in stats
        ]
