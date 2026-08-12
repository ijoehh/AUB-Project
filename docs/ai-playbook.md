# Personal AI Playbook: AI-Assisted Engineering

## 1. When I Reach for AI First
I reach for AI tools when the problem has clear constraints and a well-defined verification loop:
- **Boilerplate & Schemas:** Generating repetitive Pydantic validation schemas, enum mappings, and type annotations from a clear spec.
- **Unit Test Scaffolding:** Drafting test cases for parameterized inputs, happy paths, and expected HTTP error status codes.
- **Infrastructure Templates:** Scaffolding initial Dockerfiles, `.dockerignore` files, and GitHub Actions CI workflow YAML.
- **Documentation & Review Structure:** Formatting audit logs, structuring Markdown decision notes, and summarizing verified test results.

## 2. When I Do Not Reach for AI First
I do not reach for AI first when deep contextual reasoning, architecture boundaries, or sensitive data are involved:
- **Core Architecture & Scope Boundaries:** Choosing the storage layer, defining module boundaries, or setting project trade-offs (e.g. intentionally avoiding an ORM).
- **Security & Threat Evaluation:** Deciding which security findings to act on and verifying authentication/authorization boundaries.
- **Root Cause Debugging with Incomplete Context:** Tracing complex multi-layer bugs where the AI lacks runtime logs or environment visibility.

## 3. My Non-Negotiables
- **Zero Secrets / Zero PII:** Never paste `.env` files, production API tokens, private database connection strings, or real user data into an AI tool.
- **Inspect Before Applying:** Never merge or apply AI-generated code without reviewing the diff line by line.
- **Verification is Mandatory:** Every AI suggestion must be verified by running the test suite (`pytest -v`), manual browser checks, or curl tests.
- **No Mystery Code:** If I cannot explain what a line of code does and why it is there, it does not get committed.

## 4. My Review Rules
1. **One Task per Prompt:** Generate one file, one endpoint, or one test suite at a time; avoid massive multi-file rewrites.
2. **Triaging AI Feedback:** Classify AI comments into *Useful*, *Noise*, or *Wrong* with evidence from the actual code.
3. **Prove with Break Tests:** Deliberately break a test assertion or validation check to prove that green tests are truly protecting the system.

## 5. What I Am Still Figuring Out
- **Balancing Velocity and Code Ownership:** Finding the optimal balance between rapid AI generation and maintaining deep mental models of growing codebases.
- **Team-Wide Prompt Conventions:** Establishing standardized prompt guardrails (like `AGENTS.md`) across collaborative engineering teams.

---

## Decision Card

| Category | My Approach / Rule |
| :--- | :--- |
| **New Feature** | Define user stories and constraints first; prompt for backend models -> tests -> routes -> UI sequentially. |
| **Code Review** | Use AI to spot potential gaps, then triage comments as Useful, Noise, or Wrong with code evidence. |
| **Debugging** | Provide exact error messages, commands run, and relevant files; avoid vague "fix this" prompts. |
| **Infrastructure** | Use multi-stage Docker builds, pin runtime versions, enforce non-root users, and exclude secrets via `.dockerignore`. |
| **Never Paste** | Real credentials, API keys, `.env` files, production data, or local absolute system paths. |
| **Core Golden Rule** | **AI proposes, the developer decides. The output is not complete until inspected, tested, and verified.** |
