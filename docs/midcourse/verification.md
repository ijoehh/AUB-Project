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
plugins: anyio-4.14.1
collected 17 items

tests\test_tasks.py .................                                    [100%]

============================== warnings summary ===============================
[Warnings list omitted for brevity]
======================= 17 passed, 3 warnings in 0.25s ========================
```

---

## Behavior Contract Verification (Post-Implementation)
*(To be updated after implementing Feature 1 and Feature 2)*

### Feature 1 (Due Dates) Tests Added:
* *Test 1:* `test_create_task_valid_due_date`
* *Test 2:* `test_create_task_invalid_due_date_format`
* *Test 3:* `test_filter_tasks_by_overdue`
* *Test 4:* `test_update_due_date`

### Feature 2 (Tags) Tests Added:
* *Test 1:* `test_create_task_with_tags`
* *Test 2:* `test_create_task_reject_empty_tag`
* *Test 3:* `test_update_task_preserve_tags`
* *Test 4:* `test_filter_tasks_by_tag`

---

## Break Test Evidence
*(To be updated after intentionally breaking and repairing a test to verify test sensitivity)*
