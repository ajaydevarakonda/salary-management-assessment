from decimal import Decimal

from pydantic import BaseModel


class SalaryStatsResponse(BaseModel):
    """Response shape for salary statistics of a country."""

    country: str
    minimum: Decimal
    maximum: Decimal
    average: Decimal
    employee_count: int
    currency: str


class JobTitleSalaryStatsResponse(BaseModel):
    """Response shape for average salary per job title."""

    job_title: str
    average: Decimal
    employee_count: int
    currency: str
