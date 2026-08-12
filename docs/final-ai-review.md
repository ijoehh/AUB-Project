# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
| :--- | :--- | :--- | :--- |
| AI suggested adding generic `try/except Exception` around `storage.add_task()` in `routes.py`. | **Noise** | File operations are protected by a threading lock and atomic tempfile replacement; generic try/except would swallow meaningful errors. | Rejected to keep errors transparent and adhere to course conventions. |
| AI suggested using Pydantic `field_validator` with `strip()` to reject whitespace-only titles. | **Useful** | Catches empty/blank strings reliably and returns standard FastAPI HTTP 422 responses. | Accepted and implemented in `backend/app/schemas.py`. |
| AI suggested replacing JSON file storage with SQLite and SQLAlchemy. | **Wrong** | Violates the explicit course constraint and ADR ("no database, no ORM, JSON storage only"). | Rejected immediately to maintain intended architecture. |

## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
| :--- | :--- | :--- | :--- | :--- |
| Unbounded `assignee` field | `backend/app/schemas.py:14` | **Valid** | While `title` (200) and `description` (2000) have max length bounds, `assignee` was unconstrained, permitting oversized payloads. | Logged in backlog to add `max_length=100`. |
| Missing authentication / access control | `backend/app/main.py` | **Noise** | The lack of auth is an intentional, documented course-scope decision in `AGENTS.md` and `README.md`, not an accidental oversight. | Retained as accepted scope design. |
| Wildcard CORS with credentials enabled | `backend/app/main.py:21-28` | **Valid** | Combining `allow_origins=["*"]` with `allow_credentials=True` violates browser security standards for credentialed requests. | Documented in security review notes for future auth integration. |

## Manual security check
I manually inspected the frontend rendering logic in `frontend/index.html` to verify Cross-Site Scripting (XSS) protections. I verified that dynamic task fields (`title`, `description`, `assignee`) are processed through the `escapeHtml()` function before being injected into the DOM, preventing script injection from malicious task content.

## One AI output I rejected or corrected
When generating task update handling, the AI initially proposed allowing client updates without validating state transitions on the backend. I rejected this approach and enforced the transition matrix in `backend/app/business_rules.py` during `PATCH /tasks/{id}`, ensuring illegal status jumps (e.g. `To Do` directly to `Done`) are rejected with HTTP 422.

## Three AI usage rules
1. **Never paste:** Never paste `.env` files, API keys, credentials, or real user data into an AI tool; always use synthetic mock fixtures.
2. **Always verify:** Always run `python -m pytest -v`, inspect file diffs line by line, and run a Break Test to confirm test sensitivity before merging.
3. **Record AI contributions by:** Logging the prompt, files modified, and explicit decisions on what was accepted, edited, or rejected in `docs/`.

## Ownership statement
I have inspected, run, tested, and reviewed every component of this repository. I understand each route, Pydantic validator, business transition rule, CI workflow step, and Docker configuration line by line. AI tools were used under strict constraints to assist in drafting, but I reviewed, tested, and stand behind all code and documentation submitted.
