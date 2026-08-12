# Release Evidence

## Baseline
- Branch: final-project
- Date: August 12, 2026
- Local app run command: `python -m uvicorn app.main:app --reload` (run from `backend/`)
- /health result: HTTP 200 `{"status": "ok"}`
- Frontend check: Opened `frontend/index.html` directly in browser; confirmed the 3-column Kanban board (To Do, In Progress, Done), drag-and-drop cards, and create/edit modal form load cleanly.
- Test command: `python -m pytest -v` (run from `backend/`)
- Test result: 17 passed in 0.25s (all baseline CRUD, status transition, and validation tests pass).

## CI evidence
- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: CI workflow runs on GitHub Actions Ubuntu runner with Python 3.11, sets `PYTHONPATH: .`, and runs `python -m pytest -v` with all tests passing.
- Test command used by CI: `python -m pytest -v`
- Shortcut check: No `continue-on-error` used; no `|| true` used; no `--exit-zero` used; pytest is not skipped or masked.

## Docker evidence
- Build command: `docker build -t task-tracker:dev .`
- Run command: `docker run -d -p 8000:8000 --name tt-dev task-tracker:dev`
- /health check: `curl http://127.0.0.1:8000/health` returns `{"status": "ok"}` with HTTP 200 status code.
- Non-root check, if implemented: `docker exec tt-dev whoami` returns `app` (verified running as non-root user with UID 1000).
- No-baked-secrets check: Checked `.dockerignore` to confirm `.env`, `.env.*`, `.git`, caches, and credentials are excluded from the build context; image layers copy only virtualenv from builder stage and application source code.

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
| :--- | :--- | :--- | :--- |
| API exposes `GET /health` returning `{"status": "ok"}` | Inspected `backend/app/main.py:32-34` and tested via `curl http://127.0.0.1:8000/health` | Matches | Verified endpoint decorator and response shape. |
| Status transitions enforce valid paths (`ToDo -> InProgress -> Done`) | Tested with `tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422` | Matches | Confirmed `business_rules.py` returns HTTP 422 for invalid direct transitions. |
| Deleting a task returns HTTP 204 with no content body | Inspected `backend/app/routes.py:25-28` and ran `test_delete_existing_returns_204_no_body` | Matches | Confirmed status 204 returns empty byte response (`b""`). |
