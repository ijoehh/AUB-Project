# Verification Log

This document records the automated and manual verification results for the mid-course project.

## 1. Baseline Verification (Before Changes)

* **Date:** August 6, 2026
* **Branch:** `mid-course-project`
* **Command run:** `python -m pytest` inside the `backend/` directory.

### Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\joeha\Desktop\AUB\prototype 4\backend
collected 17 items

tests\test_tasks.py .................                                    [100%]
======================= 17 passed, 3 warnings in 0.25s ========================
```

---

## 2. Behavior Contract Verification (Post-Implementation)

* **Date:** August 10, 2026
* **Command run:** `python -m pytest` inside the `backend/` directory.
* **Results:** **32 passed** (17 baseline tests + 8 due date tests + 3 backend filter tests + 4 tags validation tests).

### Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\joeha\Desktop\AUB\prototype 4\backend
plugins: anyio-4.14.1
collected 32 items

tests\test_tasks.py ................................                     [100%]
======================= 32 passed, 3 warnings in 0.59s ========================
```

### Complete Test Inventory:

#### Baseline Tests (17):
* `test_create_task_valid_returns_201_with_full_body`
* `test_create_task_missing_title_returns_422`
* `test_create_task_blank_title_returns_422`
* `test_create_task_invalid_priority_returns_422`
* `test_create_task_unknown_field_returns_422`
* `test_list_tasks_empty_returns_200_and_empty_list`
* `test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list`
* `test_list_tasks_filter_by_priority_returns_only_matches`
* `test_get_task_by_id_returns_task`
* `test_get_task_by_id_not_found_returns_404_with_detail`
* `test_patch_partial_update_keeps_other_fields`
* `test_patch_not_found_returns_404`
* `test_patch_valid_transition_todo_to_inprogress_returns_200`
* `test_patch_invalid_transition_todo_to_done_returns_422`
* `test_patch_same_status_returns_422`
* `test_delete_existing_returns_204_no_body`
* `test_delete_missing_returns_404`

#### Feature 1: Due Date Tests (8):
* `test_create_task_with_valid_due_date`
* `test_create_task_with_invalid_due_date_format_returns_422`
* `test_create_task_with_non_date_string_due_date_returns_422`
* `test_create_task_with_null_due_date`
* `test_create_task_with_empty_due_date`
* `test_update_due_date_valid`
* `test_update_due_date_invalid_returns_422`
* `test_update_due_date_to_none`

#### Backend Filter Tests (3):
* `test_list_tasks_filter_by_tag`
* `test_list_tasks_filter_by_tag_no_match_returns_empty_list`
* `test_list_tasks_filter_by_overdue`

#### Feature 2: Tags & Labels Tests (4):
* `test_create_task_with_valid_tags`
* `test_create_task_tag_over_length_limit`
* `test_create_task_tag_count_limit`
* `test_update_task_preserves_tags`

---

## 3. Manual Browser Verification

1. **Due Date Creation & Edit:**
   * Opened Create Modal -> Entered title and due date -> Submitted -> Verified due date appears on card.
   * Clicked Edit on card -> Form loaded with existing due date -> Changed due date -> Saved -> Card updated immediately.
2. **Overdue Indicator:**
   * Created task with yesterday's date in `todo` status -> Verified red "Overdue" pill badge appears on the card.
   * Moved overdue task to `done` -> Verified "Overdue" badge disappears.
3. **Overdue Filter:**
   * Checked "Show Overdue Only" toggle -> Non-overdue tasks were hidden, only overdue tasks remained visible.
4. **Tag Filtering:**
   * Created tasks with tags `Frontend` and `Backend`.
   * Selected `Frontend` in the tag filter dropdown -> Only `Frontend` tasks were displayed.
   * Selected "All Tags" -> All tasks restored.

---

## 4. Break Test Evidence

To verify test sensitivity and regression protection, we conducted a Break Test on the tag length validation.

### Step 1: Break Introduced
In `backend/app/schemas.py`, we temporarily bypassed the tag length check inside `_validate_tags`:
```diff
-            if len(stripped) > 20:
+            if False: # len(stripped) > 20:
                 raise ValueError("Tag must be 20 characters or fewer")
```

### Step 2: Test Expected to Fail
* `tests/test_tasks.py::test_create_task_tag_over_length_limit`

### Step 3: Pytest Failure Output
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
FAILED tests/test_tasks.py::test_create_task_tag_over_length_limit - assert 201 == 422
================== 1 failed, 31 passed, 3 warnings in 0.54s ===================
```

### Step 4: Code Restored
Restored the validator check `if len(stripped) > 20:`, re-ran `pytest`, and confirmed all **32 tests passed**.
