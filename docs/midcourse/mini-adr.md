# Architectural Decision Record (ADR)

This document outlines the design choices and trade-offs for the features implemented in the mid-course project.

## Context

The Task Tracker is designed to be lightweight, with **no database, no ORM, and no Docker**—relying purely on standard file storage (`tasks.json`). The mid-course requirements call for adding two features: **Due Dates** and **Tags/Labels**.

---

## Decision 1: Storing, Validating, and Filtering Due Dates

* **Storage Format:** Store the due date as an ISO-8601 date string (`YYYY-MM-DD`) in `tasks.json`.
* **Backend Validation:** Validated via Pydantic validator (`datetime.strptime(v, "%Y-%m-%d")`). Rejects invalid dates or invalid formats with `HTTP 422`.
* **Overdue Filtering (Backend + Frontend):**
  - **Backend Filtering:** `GET /api/tasks?overdue=true` (and `GET /tasks?overdue=true`) filters and returns only tasks with a due date prior to today's UTC date where status is not `done`. Tested with automated pytest tests.
  - **Frontend Filtering:** The UI includes a "Show Overdue Only" toggle that computes overdue status relative to client local time and immediately filters the Kanban board without requiring a page reload.
* **Alternatives Rejected:**
  - *Database-stored `is_overdue` flag:* Storing a static `is_overdue` boolean in the JSON file was rejected because it would quickly become stale and would require periodic cron jobs or worker processes to stay accurate.

---

## Decision 2: Storing, Validating, and Filtering Tags

* **Storage Format:** Store tags as a native list of strings (`["Bug", "Frontend"]`) on each task record in `tasks.json`.
* **Backend Validation:** Validated via Pydantic validator in `schemas.py`:
  - Strips whitespace from each tag.
  - Discards empty strings.
  - Enforces a maximum of 5 unique tags per task.
  - Enforces a maximum length of 20 characters per tag.
* **Tag Filtering (Backend + Frontend):**
  - **Backend Filtering:** `GET /api/tasks?tag=<name>` returns only tasks containing the specified tag. Tested with automated pytest tests.
  - **Frontend Filtering:** The UI dynamically extracts all unique tags from loaded tasks, populates a filter dropdown, and filters the board on change.
* **Alternatives Rejected:**
  - *Comma-separated string in JSON:* Storing tags as a plain string (e.g. `"Bug,Frontend"`) was rejected because a JSON array directly matches Python's `list[str]` and prevents repetitive string parsing inside storage functions.

---

## Alternative AI Suggestions Rejected

1. **Vite + React Refactor:** The AI initially suggested refactoring the frontend into React/Vite. We rejected this to keep the single-file HTML/CSS/JS frontend matching Modules 1-3.
2. **Third-Party Date Picker Library:** We rejected external calendar libraries in favor of standard HTML `<input type="date">`.
3. **Transition to SQLite:** We rejected transitioning to SQLite to maintain the ADR of "no database" established in Module 3.
