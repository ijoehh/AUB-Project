# Mid-Course Reflection

This document contains a reflection on the AI-assisted development workflow used during this project.

## AI Tools Used
We used Google Antigravity (a Gemini-based agentic AI coding assistant) to plan, structure, and implement the features. We also used pytest for test verification and standard Python/JS utilities.

## Moment AI Helped
The AI was extremely helpful in structuring the Pydantic validation schemas. For example, writing the field validator to strip whitespaces, ignore empty strings, and enforce bounds (max 5 tags, max 20 characters per tag) was written in seconds and integrated perfectly with FastAPI's automatic `422` error handling.

## Moment AI Slowed Us Down
Initially, the AI proposed writing a complex background scheduler on the backend to constantly check and update whether a task is "overdue". This would have introduced database columns, state management issues, and timezone synchronization bugs between the server and the browser client. Recognizing this early and correcting the AI's assumption (by moving the overdue calculation to the client UI) saved a significant amount of development and debugging time.

## Moment Review Changed the Result
Reviewing the test suite run highlighted that we needed to run `python -m pytest` instead of just `pytest` because of system environment path configurations on Windows. Furthermore, during code review of the frontend, we refactored the tag inputs to automatically parse commas and strip excess spaces on the client side, ensuring a cleaner payload was sent to the FastAPI server.
