from __future__ import annotations
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .models import TaskCreate, TaskUpdate

# DATA_FILE location: backend/data/tasks.json
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_file() -> None:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps({"next_id": 1, "tasks": []}, indent=2))


def _read_raw() -> dict[str, Any]:
    _ensure_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_raw(data: dict[str, Any]) -> None:
    tmp = DATA_FILE.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    tmp.replace(DATA_FILE)


def get_all_tasks(status: Optional[str] = None, priority: Optional[str] = None) -> list[dict[str, Any]]:
    with _lock:
        tasks = _read_raw()["tasks"]
    if status is not None:
        tasks = [t for t in tasks if t.get("status") == status]
    if priority is not None:
        tasks = [t for t in tasks if t.get("priority") == priority]
    return tasks


def get_task_by_id(task_id: str | int) -> Optional[dict[str, Any]]:
    try:
        int_id = int(task_id)
    except (ValueError, TypeError):
        return None
    with _lock:
        for task in _read_raw()["tasks"]:
            if task["id"] == int_id:
                return task
    return None


def add_task(payload: TaskCreate) -> dict[str, Any]:
    with _lock:
        data = _read_raw()
        task_id = data["next_id"]
        now = _now()
        task = {
            "id": task_id,
            "title": payload.title,
            "description": payload.description or "",
            "status": payload.status.value if hasattr(payload.status, "value") else payload.status,
            "priority": payload.priority.value if hasattr(payload.priority, "value") else payload.priority,
            "assignee": payload.assignee,
            "due_date": payload.due_date,
            "created_at": now,
            "updated_at": now,
        }
        data["tasks"].append(task)
        data["next_id"] = task_id + 1
        _write_raw(data)
        return task


def update_task(task_id: str | int, payload: TaskUpdate) -> Optional[dict[str, Any]]:
    try:
        int_id = int(task_id)
    except (ValueError, TypeError):
        return None
    
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        return get_task_by_id(task_id)
        
    with _lock:
        data = _read_raw()
        for task in data["tasks"]:
            if task["id"] == int_id:
                for k, v in list(changes.items()):
                    if hasattr(v, "value"):
                        changes[k] = v.value
                task.update(changes)
                task["updated_at"] = _now()
                _write_raw(data)
                return task
    return None


def delete_task(task_id: str | int) -> bool:
    try:
        int_id = int(task_id)
    except (ValueError, TypeError):
        return False
    with _lock:
        data = _read_raw()
        before = len(data["tasks"])
        data["tasks"] = [t for t in data["tasks"] if t["id"] != int_id]
        if len(data["tasks"]) == before:
            return False
        _write_raw(data)
        return True
