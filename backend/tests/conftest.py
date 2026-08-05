import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import storage

# Ensure storage has _reset method dynamically if not present
if not hasattr(storage, "_reset"):
    def _reset():
        with storage._lock:
            storage._write_raw({"next_id": 1, "tasks": []})
    storage._reset = _reset

@pytest.fixture(autouse=True)
def _reset_storage():
    storage._reset()
    yield
    storage._reset()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def created_task(client):
    response = client.post("/tasks", json={"title": "fixture task"})
    assert response.status_code == 201
    return response.json()
