# Task Tracker — Architecture Document

## 1. What the App Does
Task Tracker is a lightweight single-user task management web application. It provides an interactive Kanban-style interface for organizing tasks across workflow stages (`todo`, `doing`, `done`), backed by a FastAPI REST API that persists data directly to a local JSON file without a database or ORM.

---

## 2. Data Model
The domain consists of a single primary entity, **Task**, stored in a top-level container structure:

* **Storage Container** (`backend/data/tasks.json`):
  * `next_id` (`int`): Auto-incrementing integer sequence counter.
  * `tasks` (`list[Task]`): Array of stored task records.

* **Task Entity**:
  * `id` (`int`): Unique sequential identifier generated on creation.
  * `title` (`str`, required): Task summary (1–200 characters, whitespace-trimmed, cannot be blank).
  * `description` (`str`, optional): Detailed notes (max 2,000 characters; defaults to empty string `""`).
  * `status` (`TaskStatus` enum): Current lifecycle state — `todo` (`To Do`), `doing` (`InProgress`), or `done` (`Done`). Defaults to `todo`.
  * `priority` (`TaskPriority` enum): Urgency level — `Low`, `Medium`, or `High`. Defaults to `Medium`.
  * `assignee` (`str | None`, optional): Name of the assigned user. Defaults to `None`.
  * `created_at` (`str` / ISO 8601 UTC datetime): Server-generated creation timestamp.
  * `updated_at` (`str` / ISO 8601 UTC datetime): Server-generated last-modified timestamp.

---

## 3. Request Flow: Task Creation
1. **User Action**: The user submits the task creation form on the frontend Kanban board.
2. **HTTP Request**: Frontend dispatches a `POST` request with a JSON payload (`TaskCreate`: `title`, `description`, `status`, `priority`, `assignee`) to `/tasks` (or `/api/tasks`).
3. **Pydantic Validation**: FastAPI parses and validates the payload using `TaskCreate`. It enforces non-blank trimmed titles (1–200 chars), max description length (2,000 chars), valid enum values, and forbids extraneous payload fields (returning `422 Unprocessable Entity` on failure).
4. **Storage Layer Processing**: The endpoint passes validated data to `storage.add_task()`:
   * Acquires a process-level `threading.Lock`.
   * Reads raw JSON state from `backend/data/tasks.json`.
   * Allocates `id` from `next_id` and increments the counter.
   * Attaches UTC ISO `created_at` and `updated_at` timestamps.
   * Appends the new task to the array and atomically writes the payload via a temporary file (`tasks.json.tmp` replaced to `tasks.json`).
   * Releases lock and returns the created task dictionary.
5. **HTTP Response**: Server responds with HTTP `201 Created` containing the full `TaskResponse` JSON object.
6. **UI Update**: The frontend appends the new task card to the corresponding column without requiring a full page refresh.

---

## 4. Key Files
* [`AGENTS.md`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/AGENTS.md): Defines project rules, stack constraints, status/priority values, and test commands.
* [`backend/app/main.py`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/backend/app/main.py): Sets up FastAPI instance, CORS middleware, router registration, and top-level endpoints (`/health`, `/tasks`).
* [`backend/app/models.py`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/backend/app/models.py): Defines domain representations, `TaskStatus`, `TaskPriority`, and response schemas.
* [`backend/app/schemas.py`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/backend/app/schemas.py): Pydantic input schemas (`TaskCreate`, `TaskUpdate`) with field validators and strict configurations (`extra="forbid"`).
* [`backend/app/routes.py`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/backend/app/routes.py): Declares RESTful CRUD endpoints under `/api/tasks` for filtering, retrieving, updating, and deleting tasks.
* [`backend/app/storage.py`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/backend/app/storage.py): Implements atomic, thread-safe JSON file I/O operations with `threading.Lock`.
* [`backend/app/business_rules.py`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/backend/app/business_rules.py): Enforces state-machine rules for valid status transitions (`todo` <-> `doing` <-> `done`).
* [`backend/tests/test_tasks.py`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/backend/tests/test_tasks.py): Pytest test suite covering CRUD operations, status transitions, schema constraints, and error codes.
* [`frontend/index.html`](file:///C:/Users/joeha/Desktop/AUB/prototype%204/frontend/index.html): Vanilla HTML/CSS/JavaScript single-page Kanban UI for interactive task management.

---

## 5. Conventions
* **Validation**: Request payloads are strictly validated using Pydantic v2 schemas (`extra="forbid"`, custom `@field_validator` for non-blank strings). Business rules validate status transitions (`todo` -> `doing` -> `done`, `done` -> `doing`).
* **Storage**: Flat-file JSON persistence in `backend/data/tasks.json` using Python's standard library (`json`, `pathlib`). Concurrency safety within a single process is handled via `threading.Lock()` and atomic temp file rename (`tmp.replace(DATA_FILE)`).
* **Error Handling**: Standard HTTP status codes (`201` for creation, `204` for deletion, `404` for missing tasks, `422` for invalid fields or illegal status transitions) returning standard FastAPI error payloads (`{"detail": ...}`).
* **Frontend/Backend Interaction**: Asynchronous JSON messaging via standard browser `fetch()` calls. CORS middleware enables open communication across local ports during development.

---

## 6. Not Visible or Assumptions
* **Multi-Process Concurrency**: Concurrency locking is in-memory (`threading.Lock`), which does not protect against race conditions across multiple Uvicorn worker processes (`--workers > 1`).
* **Authentication & Access Control**: No authentication, authorization, or multi-tenant scoping exists; all clients accessing the host have full read/write access.
* **Dual Endpoint Routing**: Endpoints are defined both at `/tasks` in `main.py` and under `/api/tasks` in `routes.py`.
