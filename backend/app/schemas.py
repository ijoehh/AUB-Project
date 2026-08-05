from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from .models import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False, extra="forbid")

    title: str
    description: str = Field("", max_length=2000)
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def _title_not_blank(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("Title is required and cannot be blank")
        if len(v2) > 200:
            raise ValueError("Title must be 200 characters or fewer")
        return v2


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def _title_not_blank(cls, v):
        if v is None:
            return v
        v2 = v.strip()
        if not v2:
            raise ValueError("Title is required and cannot be blank")
        if len(v2) > 200:
            raise ValueError("Title must be 200 characters or fewer")
        return v2
