from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TaskStatus(str, Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

    # Uppercase aliases for backward compatibility (e.g. if tests/verify_a.py or routes use them)
    TODO = "todo"
    IN_PROGRESS = "doing"
    DONE = "done"

class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    created_at: datetime
    updated_at: datetime

TaskResponse = Task

# Import schemas for compatibility with imports like: from app.models import TaskCreate
# Placed at the end of the file to resolve circular dependency
from .schemas import TaskCreate, TaskUpdate
