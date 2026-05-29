from dataclasses import replace
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.dependencies import get_current_user, get_employee_repository
from src.api.schemas.employee import (
    CreateEmployeeRequest,
    EmployeePageResponse,
    EmployeeResponse,
    UpdateEmployeeRequest,
)
from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository
from src.use_cases.add_employee import AddEmployee
from src.use_cases.delete_employee import DeleteEmployee
from src.use_cases.get_employee import GetEmployee
from src.use_cases.list_employees import ListEmployees
from src.use_cases.update_employee import UpdateEmployee

router = APIRouter(
    prefix="/api/employees",
    tags=["employees"],
    dependencies=[Depends(get_current_user)],
)


def _to_response(employee: Employee) -> EmployeeResponse:
    """Map a domain Employee to an EmployeeResponse."""
    return EmployeeResponse(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        job_title=employee.job_title,
        department=employee.department,
        country=employee.country,
        email=employee.email,
        salary=employee.salary,
        hire_date=employee.hire_date,
    )


def _to_domain(body: CreateEmployeeRequest | UpdateEmployeeRequest) -> Employee:
    """Map a body schema to a domain Employee."""
    return Employee(
        first_name=body.first_name,
        last_name=body.last_name,
        job_title=body.job_title,
        department=body.department,
        country=body.country,
        email=body.email,
        salary=body.salary,
        hire_date=body.hire_date,
    )


@router.post("", status_code=201, response_model=EmployeeResponse)
def create_employee(
    body: CreateEmployeeRequest,
    repository: EmployeeRepository = Depends(get_employee_repository),
):
    """Add a new employee."""
    employee = AddEmployee(repository).execute(_to_domain(body))
    return _to_response(employee)


@router.get("", response_model=EmployeePageResponse)
def list_employees(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str = Query(default=""),
    repository: EmployeeRepository = Depends(get_employee_repository),
):
    """Return a paginated, optionally filtered list of employees."""
    employees, total = ListEmployees(repository).execute_page(page, page_size, search)
    return EmployeePageResponse(
        employees=[_to_response(e) for e in employees],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    repository: EmployeeRepository = Depends(get_employee_repository),
):
    """Return a single employee by id."""
    employee = GetEmployee(repository).execute(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return _to_response(employee)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    body: UpdateEmployeeRequest,
    repository: EmployeeRepository = Depends(get_employee_repository),
):
    """Update an existing employee."""
    existing = GetEmployee(repository).execute(employee_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated = replace(_to_domain(body), id=employee_id)
    return _to_response(UpdateEmployee(repository).execute(updated))


@router.delete("/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    repository: EmployeeRepository = Depends(get_employee_repository),
):
    """Delete an employee by id."""
    if GetEmployee(repository).execute(employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    DeleteEmployee(repository).execute(employee_id)
