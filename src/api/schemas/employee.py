from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class CreateEmployeeRequest(BaseModel):
    """Payload for creating a new employee."""

    first_name: str
    last_name: str
    job_title: str
    department: str
    country: str
    email: str
    salary: Decimal
    hire_date: date


class UpdateEmployeeRequest(BaseModel):
    """Payload for updating an existing employee."""

    first_name: str
    last_name: str
    job_title: str
    department: str
    country: str
    email: str
    salary: Decimal
    hire_date: date


class EmployeeResponse(BaseModel):
    """Response shape for a single employee."""

    id: Optional[int]
    first_name: str
    last_name: str
    job_title: str
    department: str
    country: str
    email: str
    salary: Decimal
    hire_date: date


class EmployeePageResponse(BaseModel):
    """Response shape for a paginated list of employees."""

    employees: list[EmployeeResponse]
    total: int
    page: int
    page_size: int
