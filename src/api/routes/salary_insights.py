from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import (
    get_currency_converter,
    get_current_user,
    get_salary_insights_repository,
)
from src.api.schemas.salary_insights import (
    JobTitleSalaryStatsResponse,
    SalaryStatsResponse,
)
from src.domain.currency_converter import CurrencyConverter
from src.domain.salary_insights_repository import SalaryInsightsRepository
from src.use_cases.get_average_salary_by_job_title import GetAverageSalaryByJobTitle
from src.use_cases.get_salary_stats_by_country import GetSalaryStatsByCountry

router = APIRouter(
    prefix="/api/insights",
    tags=["insights"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/salary-stats", response_model=list[SalaryStatsResponse])
def get_salary_stats(
    country: str,
    repository: SalaryInsightsRepository = Depends(get_salary_insights_repository),
    converter: CurrencyConverter = Depends(get_currency_converter),
):
    """Return min, max, and average salary for a country, converted to USD."""
    result = GetSalaryStatsByCountry(repository, converter).execute(country)
    if not result:
        raise HTTPException(status_code=404, detail="No employees found for country")
    return result


@router.get("/salary-by-job-title", response_model=list[JobTitleSalaryStatsResponse])
def get_salary_by_job_title(
    country: str,
    repository: SalaryInsightsRepository = Depends(get_salary_insights_repository),
    converter: CurrencyConverter = Depends(get_currency_converter),
):
    """Return average salary per job title for a country, converted to USD."""
    result = GetAverageSalaryByJobTitle(repository, converter).execute(country)
    if not result:
        raise HTTPException(status_code=404, detail="No employees found for country")
    return result
