# AI Prompt Log

This document records the prompts used to direct the AI agents, including the weak-to-strong prompt transformations, AI responses, and developer decisions.

---

## Feature 1: Due Dates + Overdue Filter

### Prompt 1.1: Backend Schema & Storage for Due Dates
* **Weak version:** Add a due date to the backend models.
* **Improved version:**
  ```text
  You are a senior Python backend engineer. Add support for an optional due date field to the Task Tracker data model.

  Context files:
  @app/models.py
  @app/schemas.py
  @app/storage.py

  Task:
  Update the database models, schemas, and storage functions to support an optional due date.

  Exact specification:
  - FILE 1 - app/models.py:
    - Add `due_date: Optional[str] = None` to the `Task` model. The value should be stored as a string (`YYYY-MM-DD` format) in `tasks.json` or `None` if not set.
  - FILE 2 - app/schemas.py:
    - Add `due_date: Optional[str] = None` to `TaskCreate` and `TaskUpdate` models.
    - Add a field validator in Pydantic v2 syntax for `due_date` that:
      - Returns the date string as-is if it is None or empty.
      - Validates that non-empty values are in the correct `YYYY-MM-DD` format. If invalid, raise a `ValueError` which Pydantic/FastAPI will map to a 422 error.
  - FILE 3 - app/storage.py:
    - Update `add_task` to include `due_date` in the task dict created.
    - Update `update_task` to merge `due_date` correctly when it's passed in the payload.

  Constraints:
  - DO NOT use any ORM, SQLAlchemy, SQLModel, or a real database (SQLite, Postgres, etc.). Preserve the existing JSON file storage logic.
  - DO NOT add API routes in this step.
  - DO NOT import external date/time libraries unless part of Python standard library (`datetime`, `typing`).

  Output format:
  Output the complete updated content of the three modified files in separate code blocks.
  ```
* **AI Output:** The AI generated the exact code changes for `models.py`, `schemas.py`, and `storage.py` introducing `due_date` as an optional string with the `strptime` YYYY-MM-DD validator.
* **Decision/Actions:** Accepted all generated code as it followed the strict Pydantic v2 syntax. Saved the changes.

---

### Prompt 1.2: Backend Unit Tests for Due Dates
* **Weak version:** Write tests for the due date.
* **Improved version:**
  ```text
  You are a senior Python backend engineer writing pytest tests for a FastAPI app.

  Context files:
  @app/models.py
  @app/schemas.py
  @tests/test_tasks.py

  Task:
  Generate exactly 4 new unit tests in `tests/test_tasks.py` to verify the due date feature.

  Exact specification:
  - Test 1: `test_create_task_valid_due_date`
    - Creates a task with a valid due date (e.g. `"2026-08-31"`). Assert status code is 201 and `due_date` matches in the response.
  - Test 2: `test_create_task_invalid_due_date_format`
    - Tries to create a task with an invalid due date string (e.g. `"not-a-date"`). Assert status code is 422.
  - Test 3: `test_update_due_date`
    - Updates an existing task's due date to a new valid date (e.g. `"2026-09-15"`). Assert status code is 200 and the date updates.
  - Test 4: `test_clear_due_date`
    - Clears an existing task's due date by updating it to `None` or an empty string. Assert status code is 200 and `due_date` is `None` in the response.

  Constraints:
  - Use `TestClient` only. Do not use `AsyncClient`.
  - Rely on the existing storage reset fixtures in `conftest.py`.
  - DO NOT modify existing tests.

  Output format:
  Output only the test functions to be appended to `tests/test_tasks.py`.
  ```
* **AI Output:** The AI drafted exactly 4 tests matching the signatures and assertions specified.
* **Decision/Actions:** Appended them to `test_tasks.py`. Executed `python -m pytest` and all tests passed.

---

### Prompt 1.3: Frontend Integration & Overdue Filtering
* **Weak version:** Make due date work in html.
* **Improved version:**
  ```text
  You are a senior frontend developer. Add due date inputs, overdue styling, and overdue task filtering to the Task Tracker frontend.

  Context files:
  @frontend/index.html

  Task:
  Modify the single HTML file to fully support the due date feature on the client side.

  Exact specification:
  - Modal Form Changes:
    - Add a form group for "Due Date" containing `<input type="date" id="input-due-date">` inside the Create/Edit task modal.
    - Update `openCreateModal` to clear the due date input.
    - Update `openEditModal` to pre-populate the due date input with the task's existing due date.
    - Update the modal form submit listener to read the due date value and send it in the task payload.
  - Task Cards Changes:
    - In `renderBoard()`, if a task has a `due_date`, render it on the card.
    - If the task is overdue (the task's status is not `done`, and its `due_date` is in the past compared to the current date), display a prominent visual badge (red pill styled with `--priority-high` colors) labeled "Overdue".
  - Overdue Filter:
    - Add a checkbox above the Kanban board labeled "Show Overdue Only".
    - When checked, filter the tasks rendered in `renderBoard()` to show only tasks that are currently overdue. Keep the layout columns visible even if empty.

  Constraints:
  - DO NOT change the existing backend API route definitions.
  - DO NOT introduce any third-party UI libraries or CSS frameworks (like Tailwind). Use the existing CSS variables and vanilla CSS/JS.

  Output format:
  Output the complete modified `frontend/index.html` file or the exact JavaScript functions and HTML blocks to replace.
  ```
* **AI Output:** The AI generated the HTML structure, CSS styling, and JS logic for due date input, overdue badge rendering, and the checkbox filtering.
* **Decision/Actions:** Integrated the HTML/JS changes. Manually verified that tasks show overdue status correctly and filter on demand.

---

## Feature 2: Tags / Labels

### Prompt 2.1: Backend Schema & Storage for Tags
* **Weak version:** Add tags model to backend.
* **Improved version:**
  ```text
  You are a senior Python backend engineer. Add support for task categorization tags with validation limits to the data model.

  Context files:
  @app/models.py
  @app/schemas.py
  @app/storage.py

  Task:
  Update the database models, schemas, and storage functions to support an optional tags list.

  Exact specification:
  - FILE 1 - app/models.py:
    - Add `tags: list[str] = []` to the `Task` model. The tags list should be serialized as an array of strings in `tasks.json`.
  - FILE 2 - app/schemas.py:
    - Add `tags: Optional[list[str]] = None` to `TaskCreate` and `TaskUpdate`.
    - Add a field validator in Pydantic v2 syntax for `tags` that:
      - Trims/strips whitespace from each tag string.
      - Discards empty strings (`""`) from the tags list.
      - Rejects the payload (raises `ValueError`) if any tag exceeds 20 characters in length.
      - Rejects the payload (raises `ValueError`) if the total number of unique tags exceeds 5.
  - FILE 3 - app/storage.py:
    - Update `add_task` to save the validated tags list in `tasks.json` (defaulting to empty list if none provided).
    - Update `update_task` to merge and update the tags list.

  Constraints:
  - DO NOT use an ORM or database.
  - DO NOT add API routes in this step.

  Output format:
  Output the complete updated content of the three modified files in separate code blocks.
  ```
* **AI Output:** The AI generated the schema changes, including the set check for tag limits and character length bounds.
* **Decision/Actions:** Saved updates. Handled legacy tasks without a tags key by dynamically injecting `tags=[]` in `storage.py`.

---

### Prompt 2.2: Backend Unit Tests for Tags
* **Weak version:** Add test tags.
* **Improved version:**
  ```text
  You are a senior Python backend engineer writing pytest tests for a FastAPI app.

  Context files:
  @app/models.py
  @app/schemas.py
  @tests/test_tasks.py

  Task:
  Generate exactly 4 new unit tests in `tests/test_tasks.py` to verify the tags feature.

  Exact specification:
  - Test 1: `test_create_task_with_valid_tags`
    - Creates a task with a list of valid tags (e.g. `["Frontend", "Bug"]`). Assert status code is 201 and tags are returned.
  - Test 2: `test_create_task_tag_over_length_limit`
    - Tries to create a task with a tag exceeding 20 characters. Assert status code is 422.
  - Test 3: `test_create_task_tag_count_limit`
    - Tries to create a task with more than 5 tags. Assert status code is 422.
  - Test 4: `test_update_task_preserves_tags`
    - Performs a partial update (PATCH) on another field (e.g. title) of a task that has tags. Assert status code is 200 and the existing tags remain unchanged.

  Constraints:
  - Use `TestClient` only. Do not use `AsyncClient`.
  - Rely on the existing storage reset fixtures in `conftest.py`.

  Output format:
  Output only the test functions to be appended to `tests/test_tasks.py`.
  ```
* **AI Output:** AI generated the exact 4 tags verification tests.
* **Decision/Actions:** Appended tests to `test_tasks.py`. Verified that all tests pass.

---

### Prompt 2.3: Frontend Integration & Tag Filtering
* **Weak version:** Connect tag input in html.
* **Improved version:**
  ```text
  You are a senior frontend developer. Add tags input, tags chips rendering, and tag filtering to the Task Tracker frontend.

  Context files:
  @frontend/index.html

  Task:
  Modify the single HTML file to fully support the tags feature on the client side.

  Exact specification:
  - Modal Form Changes:
    - Add a form group for "Tags" containing `<input type="text" id="input-tags" placeholder="e.g. frontend, bug">` (comma-separated).
    - Update `openCreateModal` to clear the tags input.
    - Update `openEditModal` to pre-populate the tags input by joining the task's tags with commas (e.g. `"frontend, bug"`).
    - Update the modal form submit listener to read the tags input value, split it by commas, trim whitespace from each tag, remove empty values, and send the parsed array in the JSON payload.
  - Task Cards Changes:
    - Render tags as small chips/labels on task cards (use clean styling matching secondary pills, e.g. subtle background and small font size) under the description.
  - Tag Filter:
    - Add a select dropdown `<select id="filter-tag">` above the Kanban board.
    - Populate this select dropdown dynamically with all unique tags present across all tasks, plus an "All Tags" default option.
    - When a tag is selected, filter the board to show only tasks that contain that tag.

  Constraints:
  - DO NOT change the existing backend API route definitions.
  - DO NOT introduce any third-party UI libraries or CSS frameworks.

  Output format:
  Output the complete modified `frontend/index.html` file or the exact JavaScript functions and HTML blocks to replace.
  ```
* **AI Output:** AI generated the select filter, card tags container styling, modal input fields, and tag collection aggregation script.
* **Decision/Actions:** Applied changes to `index.html`. Verified dynamic dropdown options populate and filter tasks successfully.
