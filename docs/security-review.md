# Security Audit & Review Report: Task Tracker

## AI Security Audit Findings

| ID | Severity | File / location | Finding | Evidence | Suggested next step | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | **Low** | `backend/app/schemas.py:14` | **Unbounded `assignee` string length** | `assignee: Optional[str] = None` has no length restriction in `TaskCreate` or `TaskUpdate`, whereas `title` (200) and `description` (2000) are constrained. Large payloads could consume memory/disk in `tasks.json`. | Add `max_length=100` or a Pydantic field validator for `assignee`. | High |
| **SEC-02** | **Informational** | `backend/app/main.py:21-28` | **Wildcard CORS with credentials enabled** | `allow_origins=["*"]` is combined with `allow_credentials=True`. Standard browser security models reject wildcard origins when credentials are included. | If authentication/cookies are ever introduced, restrict `allow_origins` to specific trusted client URLs. | High |
| **SEC-03** | **Informational** | `backend/app/main.py`, `backend/app/routes.py` | **Absence of Authentication / Authorization** | All CRUD endpoints (`GET`, `POST`, `PATCH`, `PUT`, `DELETE`) are globally accessible with no user identification or access control. | Recognized as an intentional course-scope boundary documented in `AGENTS.md` and `README.md`. No action required for Module 5. | High |
| **SEC-04** | **Low** | `backend/app/storage.py:26-30` | **Unhandled `json.JSONDecodeError` on corrupted data file** | `_read_raw()` opens and parses `tasks.json` directly. If the file is manually edited with malformed JSON, all subsequent API calls will return unhandled HTTP 500 errors. | Wrap `json.load(f)` in a `try/except json.JSONDecodeError` block with graceful fallback or a structured error log. | High |
| **SEC-05** | **Low** | `backend/requirements.txt:1-4` | **Unpinned dependency versions (`>=` ranges)** | Packages are specified using minimum version bounds (`fastapi>=0.111`, `uvicorn[standard]>=0.30`, `pytest>=8.0.0`, `httpx>=0.27.0`) rather than pinned exact versions (`==`) or a lockfile. | Pin exact package versions or introduce a `pip-compile`/`poetry.lock` file to prevent supply-chain breaking changes. | Medium |
| **SEC-06** | **Informational** | `backend/app/routes.py:12,19,26` | **Path parameter type discrepancy (`str` vs `int`)** | `task_id` is typed as `str` in route signatures (`def g(task_id:str):`), but converted via `int(task_id)` in `storage.py`. | Type path parameters as `task_id: int` in FastAPI route signatures for automatic type validation and 422 error generation on non-integer inputs. | Medium |

### Files Inspected
* `AGENTS.md` — Guardrails, stack, and course constraints.
* `Dockerfile` — Multi-stage build, base image, user configuration, and healthcheck.
* `.dockerignore` — Excluded secrets, caches, and test artifacts.
* `.github/workflows/ci.yml` — GitHub Actions pipeline and test execution.
* `backend/requirements.txt` — Dependency specification.
* `backend/app/main.py` — FastAPI instance, CORS middleware, and endpoint handlers.
* `backend/app/routes.py` — CRUD routes and routing prefix.
* `backend/app/models.py` — Domain models and Enums (`TaskStatus`, `TaskPriority`).
* `backend/app/schemas.py` — Pydantic request models and input validation.
* `backend/app/storage.py` — JSON storage layer, file locking, and atomic writes.
* `backend/app/business_rules.py` — State transition validation logic.
* `backend/tests/test_tasks.py` & `backend/tests/conftest.py` — Test suite behavior and fixtures.
* `frontend/index.html` — Client UI, HTML escaping, and API interaction.

### Categories Where No Issues Were Found
* **Secrets & Credentials:** No hardcoded API keys, passwords, or tokens in source files; `.dockerignore` properly excludes `.env` files.
* **Docker Container Security:** Multi-stage build correctly drops build tools; non-root user `app` (UID 1000) is enforced; `python:3.11-slim` is pinned; non-destructive standard-library `HEALTHCHECK` is defined.
* **CI False-Green Risks:** `.github/workflows/ci.yml` does not contain failure-swallowing patterns like `continue-on-error`, `|| true`, or `--exit-zero`.
* **Cross-Site Scripting (XSS) in Frontend:** `frontend/index.html` sanitizes user input via an explicit `escapeHtml()` helper before inserting dynamic values (`title`, `description`, `assignee`) into the DOM.
* **Storage Concurrency & Integrity:** `storage.py` protects read-modify-write cycles with a `threading.Lock()` and performs atomic file writes via temporary file replacement (`.json.tmp -> .json`).
* **Input Injection / Schema Pollution:** Pydantic models explicitly set `extra="forbid"`, preventing mass-assignment and unexpected field injection.

### Assumptions and Limits of the Audit
* **Scope Decision on Auth & DB:** As stipulated in `AGENTS.md` and `README.md`, the lack of user authentication, multi-tenancy, and production database storage is an accepted architectural design choice for this course module rather than an accidental vulnerability.
* **Single-Process Limitation:** In-memory threading locks protect file I/O within a single worker process; multi-worker concurrency safety is out of scope per project ADR.
* **Static Read-Only Scope:** This audit was performed via static code analysis without executing active dynamic exploitation or network fuzzing.

---

## My Manual Findings

| Severity | File:Line | Finding | Suggested Fix | Reason |
| :--- | :--- | :--- | :--- | :--- |
| | | | | |

---

## Reconciliation

### Agreement
- *(Items identified by both manual review and AI audit)*

### AI-only
- **SEC-01 (Unbounded `assignee` field):** In `backend/app/schemas.py:14`, `assignee` has no length restriction.
- **SEC-02 (CORS wildcard with credentials):** In `backend/app/main.py:21-28`, `allow_origins=["*"]` is combined with `allow_credentials=True`.
- **SEC-04 (Unhandled JSON decode errors):** In `backend/app/storage.py:26-30`, corrupted `tasks.json` throws unhandled 500 errors.
- **SEC-05 (Unpinned dependencies):** In `backend/requirements.txt:1-4`, packages use loose `>=` version bounds.

### You-only
- *(Findings from your manual inspection)*

---

## Top 3 Unfixed Backlog

| Rank | Finding | Severity | Owner | Next Step |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Unbounded `assignee` field in `schemas.py` | Low | Developer | Add `max_length=100` to `TaskCreate` and `TaskUpdate`. |
| 2 | Unhandled `json.JSONDecodeError` in `storage.py` | Low | Developer | Add `try/except json.JSONDecodeError` inside `_read_raw()`. |
| 3 | Permissive CORS configuration in `main.py` | Informational | Developer | Restrict `allow_origins` to exact frontend dev URL if credentials are enabled. |
