# Salary Management

A full-stack salary management application built with FastAPI and React.

---

## Architecture

The backend follows **Clean Architecture**. Dependencies point inward — business logic has no knowledge of the database, HTTP, or any framework.

```
src/
├── domain/          # Pure Python — entities and repository interfaces
├── use_cases/       # One class per user story, orchestrates domain objects
├── infrastructure/  # MySQL repositories, JWT service, SQLAlchemy models
└── api/             # FastAPI route handlers — thin HTTP adapters
```

Each layer depends only on the layer inside it. Swapping MySQL for PostgreSQL, for example, means touching only `infrastructure/` — the domain and use cases are unaffected.

The frontend lives in `frontend/` as a plain React application (Vite), keeping backend and UI independently runnable.

---

## Why clean code lowers maintenance costs

Studies consistently show that **60–80% of the total cost of software is maintenance** — not the initial build. Every hour spent reading unfamiliar code, tracing a change through tangled layers, or fixing a bug introduced by an unrelated edit is a maintenance cost.

This project was written to keep that cost low:

- **One responsibility per class.** `AddEmployee`, `DeleteEmployee`, `UpdateEmployee` are separate use cases. A bug in deletion cannot touch addition.
- **Depend on abstractions.** Route handlers and use cases talk to repository *interfaces* (`EmployeeRepository`, `UserRepository`), not to MySQL directly. The test suite exploits this by substituting in-memory fakes — no database needed.
- **Names that read like sentences.** `GetSalaryStatsByCountry`, `LoginUser`, `mysql_employee_repository` — a new developer knows exactly where to look without reading code first.
- **No god objects.** Nothing does more than one thing. Small, focused files are easy to read in full, easy to change safely, and easy to delete when requirements change.

The result is a codebase where a change to the salary calculation touches one use case file, a change to the HTTP response shape touches one schema file, and a change to the database query touches one repository file — nothing else.

---

## What we deliberately left out

Simplicity is a feature. The following were omitted to keep the application focused:

- **No user management endpoints.** There is no API to create, update, or delete users. Users are seeded directly via the `create_sample_user` script. Adding a full user admin surface would require role-based access control, self-service password resets, and email verification — complexity that is out of scope.
- **No refresh tokens.** JWT tokens expire after 60 minutes. A refresh token flow requires a token store, rotation logic, and revocation — a meaningful security surface for a feature that is not needed here.
- **No soft deletes.** Deleted employees are removed from the database. Soft deletes add a `deleted_at` column, require every query to filter it, and introduce the concept of "restoring" records — all avoidable here.
- **No audit logging.** Who changed what and when is important in production payroll systems. It was left out to avoid coupling every write operation to a logging side-effect.

---

## Getting started

### Prerequisites

- Python 3.11+
- MySQL
- Node.js 18+

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and JWT secret

# Run migrations
alembic upgrade head

# Create a sample user
python -m scripts.create_sample_user

# Seed 10,000 employee records
python -m scripts.generates_names   # generates name lists
python -m scripts.seed              # inserts employees

# Start the API
fastapi dev src/main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` and `/auth` to `http://localhost:8000`, so no CORS configuration is needed during development.

### Tests

```bash
pytest tests/unit        # fast, no database required
pytest tests/integration # requires TEST_DATABASE_URL in .env
```

---

## API overview

All endpoints except `/auth/login` require a `Bearer` token in the `Authorization` header. A Postman collection is included at `salary_management.postman_collection.json`.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/login` | Authenticate and receive a JWT |
| GET | `/api/employees` | List all employees |
| POST | `/api/employees` | Create an employee |
| GET | `/api/employees/{id}` | Get a single employee |
| PUT | `/api/employees/{id}` | Update an employee |
| DELETE | `/api/employees/{id}` | Delete an employee |
| GET | `/api/insights/salary-stats?country=` | Min, max, avg salary and headcount by country |
| GET | `/api/insights/salary-by-job-title?country=` | Average salary per job title for a country |
