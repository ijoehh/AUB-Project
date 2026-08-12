# Task Tracker - Codex Instructions & AI Guardrails

## Tech Stack
- Python 3.11
- FastAPI (REST API backend)
- Pydantic v2 (Input validation & schemas)
- Pytest (Automated test suite)
- Vanilla JavaScript, CSS, and HTML (Frontend Kanban UI)
- Docker (Multi-stage containerization)

## Run and Test Commands
- Local API Server: `python -m uvicorn app.main:app --reload` (run from `backend/`)
- Run Tests: `python -m pytest -v` (run from `backend/`)
- Docker Build: `docker build -t task-tracker:dev .`
- Docker Run: `docker run -d -p 8000:8000 --name tt-dev task-tracker:dev`

## Project Rules & Business Logic
- Status values are `todo`, `doing`, `done` (displayed as `To Do`, `In Progress`, `Done` in the UI).
- Priority values are `Low`, `Medium`, `High`.
- State transitions are strictly validated: `To Do -> In Progress`, `In Progress -> Done`, `Done -> In Progress`. Direct jumps from `To Do` to `Done` or same-to-same transitions must return HTTP 422.
- Preserve existing API response shapes and contracts unless explicitly requested.

## AI Guardrails & Governance
1. **Read-First / Docs-First Guardrail:** Always inspect the actual source files and read existing tests before proposing code changes. Do not guess repository structure or dependencies.
2. **Plan & Diff Inspection Guardrail:** Present a clear plan and show exact file diffs before making modifications. Do not apply broad rewrites across multiple files simultaneously.
3. **Scope Control Guardrail:** Do not add authentication, multi-tenancy, production databases (SQL/ORM), cloud deployments, notifications, or unrelated UI features.
4. **Secrets & Privacy:** Never commit `.env` files, credentials, private API keys, or real personal data.
