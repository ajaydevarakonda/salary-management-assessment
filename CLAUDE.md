# Salary Management — Project Conventions

## Architecture

Clean Architecture. Dependency rule is strict: arrows point inward only.

```
src/
├── main.py                  # Entry point, wires everything together
├── domain/                  # Pure Python — no framework imports, no I/O
├── use_cases/               # One class/function per user story
├── infrastructure/          # DB, files, external APIs
└── api/routes/              # FastAPI route handlers — thin HTTP adapters

tests/
├── unit/                    # Domain + use cases, no I/O, fast
└── integration/             # API + real infrastructure
```

**domain/** knows nothing about FastAPI, the DB, or HTTP. It must stay framework-free.  
**use_cases/** orchestrates domain objects; never imports from `api/` or `infrastructure/`.  
**api/routes/** translates HTTP ↔ use case calls. No business logic here.  
**infrastructure/** holds all concrete storage/external implementations.

## Development Approach

- **TDD** — write the test first, then the minimum code to make it pass, then refactor.
- Red → Green → Refactor. No production code without a failing test first.

## Code Style — Google Python Style Guide

- **Formatter:** `black` (double quotes, 88-char line length)
- **Linter:** `pylint` with Google config
- **String quotes:** double quotes (`"`) consistently; `"""` for all docstrings
- **Indentation:** 4 spaces, never tabs
- **Line length:** 80 characters max
- **Imports:** grouped (stdlib → third-party → local), sorted lexicographically, one per line
- **Naming:** `lower_with_under` for functions/variables, `CapWords` for classes, `CAPS_WITH_UNDER` for constants
- **Docstrings:** every public function/class gets a `"""one-line summary."""`

## Clean Code Rules

- Functions do one thing. If you need "and" to describe it, split it.
- Names read like sentences — no abbreviations, no single-letter variables.
- No comments explaining *what* — names do that. Only comment *why* when non-obvious.
- Small, focused classes. No god objects.
- Depend on abstractions (Python `Protocol`), not concretions — especially at layer boundaries.
