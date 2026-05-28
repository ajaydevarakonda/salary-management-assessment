from sqlalchemy import Column, Date, Integer, Numeric, String, Index

from src.infrastructure.database import Base


class EmployeeModel(Base):
    """SQLAlchemy model for the employees table."""

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    job_title = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    salary = Column(Numeric(precision=15, scale=2), nullable=False)
    hire_date = Column(Date, nullable=False)

    __table_args__ = (
       Index("idx_employees_country", "country"),
       Index("idx_employees_job_title", "job_title"),
    )
