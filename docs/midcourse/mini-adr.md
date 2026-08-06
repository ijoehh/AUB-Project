# Architectural Decision Record (ADR)

This document outlines the design choices and trade-offs for the features implemented in the mid-course project.

## Context

The Task Tracker is designed to be lightweight, with **no database, no ORM, and no Docker**—relying purely on standard file storage (`tasks.json`). The mid-course requirements call for adding two features: **Due Dates** and **Tags/Labels**.

## Decision 1: Storing and Validating Due Dates

* **Decision:** Store the due date as an ISO-8601 date string (`YYYY-MM-DD`) in the JSON database. Use Pydantic's `date` or custom validator in the schema.
* **Backend Validation:** We validate that any non-null due date conforms to `YYYY-MM-DD` and is parsed as a valid calendar date.
* **Overdue Computation:** Instead of storing `is_overdue` in the JSON file (which would require a background job to update daily), overdue status is calculated dynamically:
  - **Frontend:** Compare the task `due_date` against the local client date at midnight.
  - **Backend:** Allow filtering GET `/tasks` by overdue status if requested.
* **Alternatives Rejected:**
  - *Storing Full Datetime/Timezones:* Storing time-of-day introduces timezone conversion complexity. Storing just `YYYY-MM-DD` represents a clean "end of day" deadline, which is simpler and robust.

---

## Decision 2: Storing and Validating Tags

* **Decision:** Store tags as a list of strings (`["Bug", "Frontend"]`) on the `Task` model.
* **Backend Validation:** Use a Pydantic validator to:
  - Strip whitespace from each tag.
  - Discard empty values.
  - Enforce a maximum of 5 tags.
  - Enforce a maximum length of 20 characters per tag.
* **Alternatives Rejected:**
  - *Normalized Comma-Separated String:* Storing tags as a comma-separated string (`"Bug,Frontend"`) in the JSON file. While this is simple, using a JSON list of strings matches native Python types and JSON structures better, avoiding repetitive splitting/joining operations.

---

## Alternative AI Suggestions Rejected

1. **Vite + React Refactor:** The AI initially suggested refactoring the frontend into React/Vite. We rejected this because a simple, single-file HTML/CSS/JS frontend matches the existing Modules 1-3 scope and avoids introducing build-system complexity.
2. **Third-Party Calendar Library:** The AI suggested importing a calendar/date picker library. We rejected this in favor of native HTML `<input type="date">` which is fully responsive and supported in all modern browsers.
3. **Transition to SQLite:** The AI suggested transitioning storage to SQLite. We rejected this to maintain the architectural decision record (ADR) of "no database" established in Module 3.
