# Sprint Retrospective - Sprint 2 (Partial)

**Date:** 2025-12-08
**Facilitator:** Scrum Master
**Participants:** Dev, Architect, PM
**Focus:** Epic 2 (User Authentication & Onboarding) - Stories 2.1 & 2.2

## 1. What Went Well
*   **Feature Delivery:** Successfully implemented core authentication features: User Registration (Story 2.1) and User Login (Story 2.2).
*   **Quality Assurance:** Both stories include comprehensive backend unit tests covering success and error scenarios. Validation reports were generated and verified.
*   **Full Stack Integration:** Frontend forms (`RegistrationForm`, `LoginForm`) were successfully connected to the backend API endpoints.
*   **Documentation:** Technical specifications and story contexts were kept up-to-date, providing clear guidance for development.

## 2. Challenges & Roadblocks
*   **Dependency Management:**
    *   Encountered several `ModuleNotFoundError` issues during testing (missing `python-multipart`, `python-jose`, `asyncpg`, `pydantic[email]`).
    *   **Critical Issue:** Version incompatibility between `passlib` (1.7.4) and `bcrypt` (4.x/5.x) caused a "password must be 72 bytes" error.
*   **Testing Infrastructure:**
    *   Initial confusion over the correct `pytest` command execution path.
    *   Missing `conftest.py` led to fixture errors in early test runs.

## 3. Action Items
*   **[High Priority] Stabilize Dependencies:**
    *   Pin working versions of `bcrypt` (4.0.1) and `passlib` in `pyproject.toml` / `requirements.txt`.
    *   Audit `requirements.txt` to ensure all runtime and dev dependencies are explicitly listed.
*   **[Medium Priority] Standardize Test Execution:**
    *   Document the exact command to run tests (e.g., `python -m pytest`) in `backend/README.md`.
    *   Ensure `conftest.py` is maintained as the source of truth for test fixtures (DB session, client).
*   **[Next Sprint] Frontend Auth State:**
    *   Prioritize Story 2.4 (NextAuth.js) to manage the JWT token securely and handle session state globally, replacing the temporary `localStorage` solution used in Story 2.2.

## 4. Status Update
*   **Story 2.1:** DONE
*   **Story 2.2:** DONE
*   **Story 2.3:** BACKLOG
*   **Story 2.4:** NEXT UP

**Conclusion:** The team successfully established the authentication foundation. Immediate focus should be on stabilizing the dependency tree to prevent future friction and moving to robust session management on the frontend.
