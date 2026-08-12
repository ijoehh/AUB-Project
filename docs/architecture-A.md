# Task Tracker — Architecture Overview

## 1. What the App Does
Task Tracker is a lightweight, single-user Kanban task management application. It provides an interactive single-page web interface for creating, viewing, updating, categorizing by priority, assigning, transitioning statuses, and deleting tasks. The system is powered by a FastAPI backend that persists state directly to a local JSON file without requiring an external database or ORM.

## 2. Data Model
* **`Task` Entity**:
  * `id` (*integer*): Unique auto-incrementing identifier (`next_id`).
  * `title` (*string*): Required, 1–200 characters, non-blank.
  * `description` (*string*): Optional details, maximum 2,000 characters (defaults to empty string).
  * `status` (*enum string*): Current workflow state (`todo`, `doing`, `done`).
  * `priority` (*enum string*): Importance level (`Low`, `Medium`, `High`; defaults to `Medium`).
  * `assignee` (*string | null*): Optional assignee name.
  * `created_at` (*ISO-8601 UTC string*): Server-generated creation timestamp.
  * `updated_at` (*ISO-8601 UTC string*): Server-generated last update timestamp.
* **Storage Schema (`tasks.json`)**:
  * Root JSON object containing `next_id` (*int*) and `tasks` (*array of `Task` objects*).

## 3. Request Flow (Task Creation)
1. **User Action**: The user submits the task form in the frontend UI (`index.html`), triggering an asynchronous `POST` request with JSON payload to the backend task creation endpoint.
2. **CORS & Routing**: FastAPI processes the request through CORS middleware and dispatches it to the route handler.
3. **Pydantic Validation**: Request data is parsed into `TaskCreate`. Pydantic strips whitespace, validates title existence/length, validates enum values, and rejects undeclared fields (`extra="forbid"`), returning `422 Unprocessable Entity` if invalid.
4. **Storage & Locking**: The handler invokes `storage.add_task()`, which acquires an in-process `threading.Lock`, reads `tasks.json`, assigns the current `next_id`, attaches UTC timestamps, increments `next_id`, and atomically writes back to disk via a temporary `.tmp` file replacement.
5. **Response & UI Update**: The server responds with `201 Created` and the serialized `Task` object; the frontend receives the JSON and dynamically renders the new task card into the Kanban board.

## 4. Key Files
* `backend/app/main.py`: FastAPI application entry point, CORS middleware setup, and top-level route definitions.
* `backend/app/routes.py`: RESTful router handling task CRUD endpoints under `/api/tasks`.
* `backend/app/models.py`: Core domain data models (`Task`, `TaskStatus`, `TaskPriority`) and response definitions.
* `backend/app/schemas.py`: Pydantic request validation schemas (`TaskCreate`, `TaskUpdate`) and field constraints.
* `backend/app/storage.py`: JSON file persistence layer managing atomic file operations and thread-safe locking.
* `backend/app/business_rules.py`: Domain validation logic enforcing permitted task status transitions.
* `backend/data/tasks.json`: Flat-file datastore holding the application state and auto-increment sequence.
* `frontend/index.html`: Standalone single-page frontend containing UI markup, styling, and vanilla JavaScript client logic.
* `backend/tests/test_tasks.py`: Pytest suite verifying endpoint status codes, schema validation, and persistence behavior.

## 5. Conventions
* **Validation**: Strict schema validation via Pydantic v2 rejecting extra parameters, validating string bounds, and enforcing explicit status lifecycle transitions.
* **Storage**: Flat-file JSON persistence utilizing `threading.Lock` and atomic file rename (`tmp.replace(DATA_FILE)`) to prevent write corruption.
* **Error Handling**: Standard HTTP status codes (`201` Created, `204` No Content, `404` Not Found, `422` Validation/Business Rule Error) with structured error detail payloads.
* **Frontend/Backend Interaction**: RESTful JSON over HTTP using native `fetch()` calls; client state is refreshed and rendered dynamically upon successful API responses.

## 6. Not Visible or Assumptions
* **Multi-Process Concurrency**: Concurrency protection uses in-memory `threading.Lock`; running multiple Uvicorn worker processes (`--workers > 1`) will cause file race conditions.
* **Authentication & Tenancy**: No authentication or multi-tenant isolation exists; all users access a single global task repository.
* **Route Redundancy**: Both `/tasks` (in `main.py`) and `/api/tasks` (in `routes.py`) exist to accommodate API versioning or legacy test suites.
