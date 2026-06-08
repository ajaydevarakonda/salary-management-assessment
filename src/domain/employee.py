from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Employee:
    """Represents an employee in the organisation."""

    first_name: str
    last_name: str
    job_title: str
    department: str
    country: str
    email: str
    salary: Decimal
    hire_date: date
    currency: str
    id: Optional[int] = None

    def __post_init__(self):
        if not self.first_name:
            raise ValueError("First name cannot be empty")
        if not self.last_name:
            raise ValueError("Last name cannot be empty")
        if self.salary <= 0:
            raise ValueError("Salary must be positive")
        if not self.currency:
            raise ValueError("Currency cannot be empty")
        if len(self.currency) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")

    def full_name(self) -> str:
        """Return the employee's full name."""
        return f"{self.first_name} {self.last_name}"
