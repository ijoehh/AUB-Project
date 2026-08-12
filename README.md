# Task Tracker

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates
- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and/or pull request.
- Docker image builds and runs with `/health` returning 200.
- AI review, security, and ownership evidence is in `docs/`.

### How to run locally
Navigate to `backend/`, install requirements, and run the server:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Open interactive Swagger docs at **http://127.0.0.1:8000/docs** or open `frontend/index.html` in your browser.

### How to run tests
Navigate to `backend/` and run pytest:
```bash
cd backend
python -m pytest -v
```

### How to run with Docker
Build and run the container from the repository root:
```bash
docker build -t task-tracker:dev .
docker run -d -p 8000:8000 --name tt-dev task-tracker:dev
curl http://127.0.0.1:8000/health
```

### Evidence files
- [`docs/release-evidence.md`](docs/release-evidence.md)
- [`docs/final-ai-review.md`](docs/final-ai-review.md)
- [`docs/ai-playbook.md`](docs/ai-playbook.md)

### AI assistance summary
- **AI helped draft or review:** CI workflow, Dockerfile, docstrings, security reviews, and test scaffolding.
- **I verified the work by:** Running automated tests (`pytest -v`), manual browser checks, testing Docker container runtime and `/health` endpoint, and performing Break Tests on business rules.
- **One AI suggestion I rejected or corrected:** Rejected AI recommendation to replace standard library JSON storage with SQLite and an ORM, preserving the course's lightweight architecture.

---

A minimal task tracker built to a specific architecture decision: **no database,
no ORM, no Docker** — just FastAPI, Pydantic, and a `tasks.json` file managed
with Python's standard library.

## Stack

- **Backend:** FastAPI + Pydantic, storing state in `backend/data/tasks.json`
  via `json` + `pathlib` only (no SQLite, no TinyDB, no SQLModel).

## Run it

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open the interactive API docs at **http://127.0.0.1:8000/docs** or access the API directly.

That's it — one dependency install, one command, run every time you want to
start the server. `backend/data/tasks.json` is created automatically on
first run if it doesn't exist yet, and you can open it in any text editor to
see exactly what the app has stored.

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
