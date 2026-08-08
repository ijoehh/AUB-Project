# Task Tracker

A minimal task tracker built to a specific architecture decision: **no database,
no ORM, no Docker** — just FastAPI, Pydantic, and a `tasks.json` file managed
with Python's standard library.

## Stack

- **Backend:** FastAPI + Pydantic, storing state in `backend/data/tasks.json`
  via `json` + `pathlib` only (no SQLite, no TinyDB, no SQLModel).

## Run and Test Instructions

### 1. Running the Backend
Navigate to the `backend/` directory, install requirements, and run the server:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
The interactive API documentation will be available at **http://127.0.0.1:8000/docs**.

### 2. Opening the Frontend
You can open `frontend/index.html` directly in any web browser. 

Alternatively, you can run a local server from the project root:
```bash
python -m http.server 5500
```
Then open **http://127.0.0.1:5500/frontend/** in your browser.

### 3. Running the Test Suite
To run the automated tests, navigate to the `backend/` directory and execute:
```bash
python -m pytest
```
All 33 tests should pass.

## API

| Method | Path              | Body               | Description              |
|--------|-------------------|--------------------|---------------------------|
| GET    | `/api/tasks`      | —                  | List all tasks            |
| POST   | `/api/tasks`      | `TaskCreate`       | Create a task              |
| GET    | `/api/tasks/{id}` | —                  | Fetch one task              |
| PUT    | `/api/tasks/{id}` | `TaskUpdate` (partial) | Update a task          |
| DELETE | `/api/tasks/{id}` | —                  | Delete a task              |

`status` is one of `todo`, `doing`, `done`. Interactive API docs are available
at `/docs` (Swagger UI, provided free by FastAPI).

## Known trade-offs (by design)

This project intentionally accepts the trade-offs documented in its ADR:

- **Concurrency:** a `threading.Lock` around each read-modify-write cycle
  prevents corruption from concurrent requests *within a single process*, but
  this is **not** safe across multiple worker processes (`--workers N`) or
  multiple machines. Don't run this in production behind multiple workers.
- **Scaling:** every write reloads and rewrites the entire `tasks.json` file.
  Fine for a learning project; not viable at scale.
- **No auth, no multi-tenancy:** anyone who can reach the server can read and
  write all tasks.

## Project structure

```
task-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app setup + CORS configuration
│   │   ├── models.py      # Domain model: Task, TaskStatus
│   │   ├── schemas.py     # Request schemas: TaskCreate, TaskUpdate
│   │   ├── storage.py     # JSON file I/O + concurrency lock
│   │   └── routes.py      # /api/tasks CRUD routes
│   ├── data/
│   │   └── tasks.json     # The database. Yes, really.
│   └── requirements.txt
└── README.md
```
