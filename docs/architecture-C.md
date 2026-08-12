# Task Tracker — Architecture Document

## 1. What the App Does
Task Tracker is a FastAPI-based backend service designed to manage tasks with status, priority, assignee, and timestamp tracking. It provides HTTP endpoints for health checks and task operations, persisting records directly to a local JSON file. Frontend capabilities and user interface workflows are not visible from the files I read.

---

## 2. Data Model
Based on `backend/app/models.py` and `backend/app/storage.py`, the core entity and storage structure are:

* **Storage Container** (`backend/data/tasks.json`):
  * `next_id` (`int`): Auto-incrementing integer identifier sequence.
  * `tasks` (`list[dict]`): Collection of serialized task records.

* **Task Entity** (`Task` / `TaskResponse`):
  * `id` (`int`): Unique numeric identifier generated on creation.
  * `title` (`str`): Title of the task (field length constraints are not visible from the files I read).
  * `description` (`str`): Task description, defaults to `""`.
  * `status` (`TaskStatus` enum): Lifecycle state — `todo`, `doing`, or `done` (aliases: `TODO`, `IN_PROGRESS`, `DONE`). Defaults to `todo`.
  * `priority` (`TaskPriority` enum): Priority level — `LOW` ("Low"), `MEDIUM` ("Medium"), or `HIGH` ("High"). Defaults to `MEDIUM`.
  * `assignee` (`str | None`): Assigned user name, defaults to `None`.
  * `created_at` (`datetime`): Timestamp of creation (stored as ISO 8601 UTC string).
  * `updated_at` (`datetime`): Timestamp of last modification (stored as ISO 8601 UTC string).

---

## 3. Request Flow: Task Creation
1. **Client Submission**: A client sends an HTTP `POST` request to `/tasks` with a JSON payload matching `TaskCreate`.
2. **Payload Parsing**: FastAPI parses the request body against the `TaskCreate` schema (detailed schema constraints are not visible from the files I read).
3. **Storage Handler**: `main.create_task` invokes `storage.add_task(payload)`.
4. **Locking & ID Generation**: `storage.py` acquires an in-process thread lock (`threading.Lock`), reads `backend/data/tasks.json`, assigns `next_id` as the task ID, and generates UTC ISO timestamps for `created_at` and `updated_at`.
5. **Persistence**: The new task dictionary is appended to `tasks`, `next_id` is incremented, and data is written to `.json.tmp` before replacing `tasks.json`.
6. **Response**: The handler returns the created record serialized as `TaskResponse` with HTTP status `201 Created`. (Client-side UI handling is not visible from the files I read).

---

## 4. Key Files
* `backend/app/main.py`: Main API entry point configuring FastAPI, CORS middleware, router inclusion, health check, and `/tasks` endpoints.
* `backend/app/models.py`: Defines data entities (`Task`), enums (`TaskStatus`, `TaskPriority`), and exports schema models.
* `backend/app/storage.py`: Flat-file JSON persistence layer implementing thread-locked CRUD helper functions.
* `backend/app/schemas.py`: Request schemas (`TaskCreate`, `TaskUpdate`) — imported by models/main, but contents not visible from the files I read.
* `backend/app/routes.py`: Additional API router included into the application — contents not visible from the files I read.
* `backend/app/business_rules.py`: Status transition validation logic — imported by main, but contents not visible from the files I read.
* `backend/data/tasks.json`: Local JSON file storing serialized task records and sequence state — referenced in storage, but not directly read.
* `frontend/index.html`: Client interface file — existence/contents not visible from the files I read.

---

## 5. Conventions
* **Validation**: Request payloads and response models are validated via Pydantic (`TaskCreate`, `TaskUpdate`, `TaskResponse`). `main.py` explicitly invokes `validate_status_transition` on PATCH requests modifying status (transition rules not visible from the files I read).
* **Storage**: Data is stored in a flat JSON file (`backend/data/tasks.json`). Concurrency safety within the process is handled using `threading.Lock()`, and atomic writes are performed via temporary `.json.tmp` file swapping.
* **Error Handling**: Missing records in `main.py` raise `HTTPException(status_code=404, detail="Not found")`. In `storage.py`, invalid/non-integer IDs return `None` or `False`. Other global exception handling is not visible from the files I read.
* **Frontend/Backend Interaction**: CORS middleware is enabled on the backend with wildcard permissions (`allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`). Frontend communication mechanisms and payloads are not visible from the files I read.

---

## 6. Not Visible or Assumptions
* **Schema Validation Details**: Specific input field constraints (e.g., character limits, regex validation, whitespace stripping, forbidden extra fields) in `schemas.py` are not visible from the files I read.
* **Status Transition Rules**: The valid state graph and constraints implemented in `business_rules.py` are not visible from the files I read.
* **Additional API Endpoints**: Endpoints declared inside `routes.py` (such as task listing or deletion routes) are not visible from the files I read.
* **Frontend Architecture**: All frontend technology, UI components, client-side routing, and rendering logic are not visible from the files I read.
* **Testing & Deployment**: Test suites, test runners, Docker configuration, and CI/CD pipelines are not visible from the files I read.
