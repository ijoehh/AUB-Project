"""
Task Tracker — FastAPI backend.

Run from inside backend/:
    python -m uvicorn app.main:app --reload
Then open:
    http://127.0.0.1:8000
"""
from __future__ import annotations

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import TaskCreate, TaskResponse, TaskUpdate
from app import storage
from app.business_rules import validate_status_transition
from .routes import router

app = FastAPI(title="Task Tracker", version="1.0.0")

# Enable CORS for development with external frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority, tag=tag, overdue=overdue)

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)

@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    if payload.status is not None:
        existing_task = storage.get_task_by_id(task_id)
        if not existing_task:
            raise HTTPException(status_code=404, detail="Not found")
        existing = TaskResponse.model_validate(existing_task)
        validate_status_transition(existing.status, payload.status)
        
    updated = storage.update_task(task_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return TaskResponse.model_validate(updated)


