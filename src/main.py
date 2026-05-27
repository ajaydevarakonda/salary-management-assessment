from fastapi import FastAPI

from src.api.routes.employee import router as employee_router

app = FastAPI(title="Salary Management")

app.include_router(employee_router)
