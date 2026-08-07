from __future__ import annotations
from datetime import datetime
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
    due_date: Optional[str] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def _title_not_blank(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("Title is required and cannot be blank")
        if len(v2) > 200:
            raise ValueError("Title must be 200 characters or fewer")
        return v2

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v
        processed_tags = []
        for tag in v:
            stripped = tag.strip()
            if stripped == "":
                continue
            if len(stripped) > 20:
                raise ValueError("Tag must be 20 characters or fewer")
            processed_tags.append(stripped)
        if len(set(processed_tags)) > 5:
            raise ValueError("Number of unique tags must not exceed 5")
        return processed_tags

    @field_validator("due_date")
    @classmethod
    def _validate_due_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return v
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("due_date must be in YYYY-MM-DD format")
        return v


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[list[str]] = None

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

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v
        processed_tags = []
        for tag in v:
            stripped = tag.strip()
            if stripped == "":
                continue
            if len(stripped) > 20:
                raise ValueError("Tag must be 20 characters or fewer")
            processed_tags.append(stripped)
        if len(set(processed_tags)) > 5:
            raise ValueError("Number of unique tags must not exceed 5")
        return processed_tags

    @field_validator("due_date")
    @classmethod
    def _validate_due_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return v
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("due_date must be in YYYY-MM-DD format")
        return v
