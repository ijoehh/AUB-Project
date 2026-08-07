import pytest

# POST /tasks
def test_create_task_valid_returns_201_with_full_body(client):
    payload = {
        "title": "valid task",
        "description": "some desc",
        "status": "todo",
        "priority": "Medium",
        "assignee": "Alice"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["id"] > 0
    assert data["title"] == "valid task"
    assert data["description"] == "some desc"
    assert data["status"] == "todo"
    assert data["priority"] == "Medium"
    assert data["assignee"] == "Alice"
    assert isinstance(data["created_at"], str)
    assert isinstance(data["updated_at"], str)

def test_create_task_missing_title_returns_422(client):
    payload = {
        "description": "missing title"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422

def test_create_task_blank_title_returns_422(client):
    payload = {
        "title": "   "
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422

def test_create_task_invalid_priority_returns_422(client):
    payload = {
        "title": "valid task",
        "priority": "SuperHigh"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422

def test_create_task_unknown_field_returns_422(client):
    payload = {
        "title": "valid task",
        "unknown_field": "something"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


# GET /tasks
def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    response = client.get("/api/tasks", params={"status": "doing"})
    assert response.status_code == 200
    assert response.json() == []

def test_list_tasks_filter_by_priority_returns_only_matches(client):
    task1 = client.post("/tasks", json={"title": "High task", "priority": "High"}).json()
    task2 = client.post("/tasks", json={"title": "Low task", "priority": "Low"}).json()
    
    response = client.get("/api/tasks", params={"priority": "High"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["id"] == task1["id"]
    assert results[0]["priority"] == "High"


# GET /tasks/{id}
def test_get_task_by_id_returns_task(client, created_task):
    task_id = created_task["id"]
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == created_task

def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/api/tasks/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


# PATCH /tasks/{id}
def test_patch_partial_update_keeps_other_fields(client, created_task):
    task_id = created_task["id"]
    payload = {"title": "updated title"}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "updated title"
    assert data["description"] == created_task["description"]
    assert data["status"] == created_task["status"]
    assert data["priority"] == created_task["priority"]
    assert data["assignee"] == created_task["assignee"]

def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/999999", json={"title": "new title"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    task_id = created_task["id"]
    payload = {"status": "doing"}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "doing"

def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    task_id = created_task["id"]
    payload = {"status": "done"}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 422

def test_patch_same_status_returns_422(client, created_task):
    task_id = created_task["id"]
    payload = {"status": "todo"}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 422


# DELETE /tasks/{id}
def test_delete_existing_returns_204_no_body(client, created_task):
    task_id = created_task["id"]
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204
    assert response.content == b""

def test_delete_missing_returns_404(client):
    response = client.delete("/api/tasks/999999")
    assert response.status_code == 404


# Optional Due Date Tests
def test_create_task_with_valid_due_date(client):
    payload = {
        "title": "task with due date",
        "due_date": "2026-12-31"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"] == "2026-12-31"

def test_create_task_with_invalid_due_date_format_returns_422(client):
    payload = {
        "title": "task with bad due date",
        "due_date": "31-12-2026"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422

def test_create_task_with_non_date_string_due_date_returns_422(client):
    payload = {
        "title": "task with bad due date",
        "due_date": "not-a-date"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422

def test_create_task_with_null_due_date(client):
    payload = {
        "title": "task with null due date",
        "due_date": None
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["due_date"] is None

def test_create_task_with_empty_due_date(client):
    payload = {
        "title": "task with empty due date",
        "due_date": ""
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["due_date"] == ""

def test_update_due_date_valid(client, created_task):
    task_id = created_task["id"]
    payload = {"due_date": "2027-01-15"}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["due_date"] == "2027-01-15"

def test_update_due_date_invalid_returns_422(client, created_task):
    task_id = created_task["id"]
    payload = {"due_date": "2027/01/15"}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 422

def test_update_due_date_to_none(client, created_task):
    task_id = created_task["id"]
    # First set it to a valid date
    client.patch(f"/tasks/{task_id}", json={"due_date": "2027-01-15"})
    # Now set it to None
    response = client.patch(f"/tasks/{task_id}", json={"due_date": None})
    assert response.status_code == 200
    assert response.json()["due_date"] is None


def test_create_task_valid_due_date(client):
    payload = {
        "title": "Valid Due Date Task",
        "due_date": "2026-08-31"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-08-31"


def test_create_task_invalid_due_date_format(client):
    payload = {
        "title": "Invalid Due Date Task",
        "due_date": "not-a-date"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_update_due_date(client, created_task):
    task_id = created_task["id"]
    payload = {"due_date": "2026-09-15"}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-09-15"


def test_clear_due_date(client, created_task):
    task_id = created_task["id"]
    # First set to a valid date
    client.patch(f"/tasks/{task_id}", json={"due_date": "2026-08-31"})
    # Clear the date
    payload = {"due_date": None}
    response = client.patch(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["due_date"] is None


def test_create_task_with_valid_tags(client):
    payload = {
        "title": "task with valid tags",
        "tags": ["Frontend", "Bug"]
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["tags"] == ["Frontend", "Bug"]


def test_create_task_tag_over_length_limit(client):
    payload = {
        "title": "task with long tag",
        "tags": ["a" * 21]
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_create_task_tag_count_limit(client):
    payload = {
        "title": "task with too many tags",
        "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_update_task_preserves_tags(client):
    # Create task with tags
    payload = {
        "title": "original task",
        "tags": ["Frontend", "Bug"]
    }
    create_resp = client.post("/tasks", json=payload)
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    # Partially update another field
    update_payload = {"title": "updated task title"}
    response = client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["tags"] == ["Frontend", "Bug"]
