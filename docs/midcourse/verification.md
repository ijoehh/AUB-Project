# Verification Log

This document records the automated and manual verification results for the mid-course project.

## Baseline Verification (Before Changes)

* **Date:** August 6, 2026
* **Branch:** `mid-course-project`
* **Command run:** `python -m pytest` inside the `backend/` directory.

### Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\joeha\Desktop\AUB\prototype 3 - removed front\backend
collected 17 items

tests\test_tasks.py .................                                    [100%]
======================= 17 passed, 3 warnings in 0.25s ========================
```

---

## Behavior Contract Verification (Post-Implementation)

* **Date:** August 7, 2026
* **Command run:** `python -m pytest` inside the `backend/` directory.
* **Results:** **33 passed** (17 original tests + 8 due date tests + 8 tags tests).

### Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\joeha\Desktop\AUB\prototype 3 - removed front\backend
plugins: anyio-4.14.1
collected 33 items

tests\test_tasks.py .................................                    [100%]
======================= 33 passed, 3 warnings in 0.50s ========================
```

### Feature 1 (Due Dates) Tests Added:
* `test_create_task_with_valid_due_date`
* `test_create_task_with_invalid_due_date_format_returns_422`
* `test_create_task_with_non_date_string_due_date_returns_422`
* `test_create_task_with_null_due_date`
* `test_create_task_with_empty_due_date`
* `test_update_due_date_valid`
* `test_update_due_date_invalid_returns_422`
* `test_update_due_date_to_none`

### Feature 2 (Tags) Tests Added:
* `test_create_task_with_valid_tags`
* `test_create_task_tag_over_length_limit`
* `test_create_task_tag_count_limit`
* `test_update_task_preserves_tags`

---

## Break Test Evidence

To prove that the unit tests are sensitive and correctly protect the system boundaries, we performed a Break Test.

### 1. Break Introduced
In `backend/app/schemas.py`, we temporarily bypassed the tag length limit check inside the Pydantic field validator for `tags`:
```diff
-            if len(stripped) > 20:
+            if False: # len(stripped) > 20:
                 raise ValueError("Tag must be 20 characters or fewer")
```

### 2. Tests Expected to Fail
* `tests/test_tasks.py::test_create_task_tag_over_length_limit` (should return 201 Created instead of 422 Unprocessable Content).

### 3. Actual Pytest Failure Output
```text
================================== FAILURES ===================================
___________________ test_create_task_tag_over_length_limit ____________________

client = <starlette.testclient.TestClient object at 0x0000020BD53B78A0>

    def test_create_task_tag_over_length_limit(client):
        payload = {
            "title": "task with long tag",
            "tags": ["a" * 21]
        }
        response = client.post("/tasks", json=payload)
>       assert response.status_code == 422
E       assert 201 == 422
E        +  where 201 = <Response [201 Created]>.status_code

tests\test_tasks.py:267: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_tasks.py::test_create_task_tag_over_length_limit - assert 2...
================== 1 failed, 32 passed, 3 warnings in 0.54s ===================
```

### 4. Restoration
We restored the tag length check validation in `backend/app/schemas.py`, ran `pytest`, and confirmed all **33 tests passed** again.
