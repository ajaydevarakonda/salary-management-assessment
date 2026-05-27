from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from src.domain.employee import Employee
from src.domain.employee_repository import EmployeeRepository
from src.infrastructure.models.employee_model import EmployeeModel


class MysqlEmployeeRepository(EmployeeRepository):
    """SQLAlchemy implementation of the EmployeeRepository protocol."""

    def __init__(self, session: Session):
        self._session = session

    def add(self, employee: Employee) -> Employee:
        """Persist a new employee and return it with its assigned id."""
        model = _to_model(employee)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return _to_domain(model)

    def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """Return the employee with the given id, or None if not found."""
        model = self._session.get(EmployeeModel, employee_id)
        return _to_domain(model) if model else None

    def find_all(self) -> list[Employee]:
        """Return all employees."""
        models = self._session.query(EmployeeModel).all()
        return [_to_domain(model) for model in models]

    def update(self, employee: Employee) -> Employee:
        """Persist changes to an existing employee and return it."""
        model = self._session.get(EmployeeModel, employee.id)
        model.first_name = employee.first_name
        model.last_name = employee.last_name
        model.job_title = employee.job_title
        model.department = employee.department
        model.country = employee.country
        model.email = employee.email
        model.salary = employee.salary
        model.hire_date = employee.hire_date
        self._session.commit()
        self._session.refresh(model)
        return _to_domain(model)

    def delete(self, employee_id: int) -> None:
        """Remove the employee with the given id."""
        model = self._session.get(EmployeeModel, employee_id)
        if model:
            self._session.delete(model)
            self._session.commit()


def _to_model(employee: Employee) -> EmployeeModel:
    """Map a domain Employee to a SQLAlchemy EmployeeModel."""
    return EmployeeModel(
        first_name=employee.first_name,
        last_name=employee.last_name,
        job_title=employee.job_title,
        department=employee.department,
        country=employee.country,
        email=employee.email,
        salary=employee.salary,
        hire_date=employee.hire_date,
    )


def _to_domain(model: EmployeeModel) -> Employee:
    """Map a SQLAlchemy EmployeeModel to a domain Employee."""
    return Employee(
        id=model.id,
        first_name=model.first_name,
        last_name=model.last_name,
        job_title=model.job_title,
        department=model.department,
        country=model.country,
        email=model.email,
        salary=Decimal(str(model.salary)),
        hire_date=model.hire_date,
    )
