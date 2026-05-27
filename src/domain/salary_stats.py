from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SalaryStats:
    """Salary statistics for all employees in a country."""

    country: str
    minimum: Decimal
    maximum: Decimal
    average: Decimal
    employee_count: int


@dataclass(frozen=True)
class JobTitleSalaryStats:
    """Average salary for a job title within a country."""

    job_title: str
    average: Decimal
    employee_count: int
