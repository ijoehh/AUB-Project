# User Stories & Acceptance Criteria

This document lists the user stories, acceptance criteria, and AI assumptions corrected for both features.

## Feature 1: Due Dates + Overdue Filter

### User Story 1: Add Due Date on Creation
* **As a** user,
* **I want to** specify an optional due date when creating a task,
* **So that** I can record its deadline from the start.
* **Acceptance Criteria:**
  - The creation form includes an optional Date input.
  - Submitting a valid `YYYY-MM-DD` date stores it in the JSON file.
  - Backend returns a `201 Created` status with the due date in the response body.
  - Submitting an invalid date format (e.g., `"not-a-date"`) returns a `422 Unprocessable Content` validation error.

### User Story 2: Update Due Date
* **As a** user,
* **I want to** update or remove a task's due date,
* **So that** I can adjust deadlines when plans change.
* **Acceptance Criteria:**
  - The task edit form allows changing the due date.
  - Sending a new date via `PATCH` updates the task and sets `updated_at`.
  - Sending an empty value/null removes the due date.

### User Story 3: Visual Overdue Indicators
* **As a** user,
* **I want to** see a clear visual indicator for overdue tasks,
* **So that** I know which tasks need immediate attention.
* **Acceptance Criteria:**
  - Tasks with a due date in the past that are NOT completed (`status` is `todo` or `doing`) display a prominent "Overdue" pill on the card.
  - Completed tasks (`status` is `done`) do NOT display an overdue pill even if the deadline is in the past.

### User Story 4: Overdue Filtering
* **As a** user,
* **I want to** filter the Kanban board to show only overdue tasks,
* **So that** I can focus exclusively on delayed items.
* **Acceptance Criteria:**
  - A checkbox/toggle is available above the board to "Show Overdue Only".
  - Checking this box hides all tasks that are not overdue.
  - Column empty states are maintained cleanly.

### AI Assumption Corrected
* **AI Assumption:** The AI assumed the overdue flag should be computed by the backend and returned as a boolean property `is_overdue` on the task model.
* **Correction:** Since the server might run in UTC but the user is viewing the board in their local timezone, calculating "overdue" dynamically in the frontend client logic (comparing task due date at local midnight to local current date) prevents timezone mismatches.

---

## Feature 2: Tags / Labels

### User Story 1: Assign Tags to Tasks
* **As a** user,
* **I want to** assign descriptive tags to a task,
* **So that** I can categorize tasks by domain or team.
* **Acceptance Criteria:**
  - Task forms include a field to add tags (entered as comma-separated values).
  - Backend accepts tags as a list of strings (`["Bug", "Frontend"]`).
  - Trimmed, empty, or duplicate tag values are handled correctly (whitespaces removed, empty tags discarded).
  - Enforce a maximum of 5 tags per task, and maximum 20 characters per tag.

### User Story 2: View Tags on Card
* **As a** user,
* **I want to** see tag chips rendered on task cards,
* **So that** I can categorize tasks visually.
* **Acceptance Criteria:**
  - Each tag is rendered as a stylized chip below the task description.
  - Chips are color-coded or use a clean secondary aesthetic that does not clash with priority badges.

### User Story 3: Filter Board by Tag
* **As a** user,
* **I want to** filter tasks by a specific tag,
* **So that** I see only tasks associated with that label.
* **Acceptance Criteria:**
  - A tag selection dropdown or filter input is placed above the board.
  - Selecting a tag shows only tasks matching that tag across all columns.
  - Selecting "All Tags" clears the filter.

### AI Assumption Corrected
* **AI Assumption:** The AI assumed tags could be arbitrary strings without length restrictions or validation.
* **Correction:** We enforced validation on the backend (using Pydantic validators) to reject tags exceeding 20 characters or tasks exceeding 5 tags, preventing UI overflow issues.
