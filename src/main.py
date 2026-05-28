from fastapi import FastAPI

from src.api.auth.routes import router as auth_router
from src.api.routes.employee import router as employee_router
from src.api.routes.salary_insights import router as salary_insights_router

app = FastAPI(title="Salary Management")

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(salary_insights_router)
