# Sprint Plan: Project Closure & Submission

**Sprint:** Closure / Hardening
**Role:** Scrum Master (SM)
**Date:** 2025-12-15
**Goal:** Finalize AI Buddy (IBE160) for submission, ensuring all MVP epics are verified, documentation is complete, and the codebase is clean and deployable.

## 1. Context & Status
- **Epics Completed:** Epics 1 through 7 are marked as done in the project plan.
- **Current Branch:** `fase-4-auth-epic-5` (Needs final merge to `main`).
- **Focus:** Verification, Documentation, and Packaging.

## 2. Sprint Backlog & Tasks

### A. QA & Code Verification
*   [ ] **Merge to Main:** Ensure all feature branches (including `fase-4-auth-epic-5`) are merged into `main`.
*   [ ] **CI Status Check:** Verify GitHub Actions (or local test suites) are GREEN for both Frontend and Backend.
    *   *Command:* `npm test` (Frontend), `pytest` (Backend).
*   [ ] **E2E Testing:** Run full Playwright suite.
    *   *Command:* `npx playwright test`
    *   *Known Issue:* Verify "dashboard test skip" is properly documented or resolved (if critical).
*   [ ] **Accessibility Audit:** Run final accessibility check (Story 7.1).
    *   *Tool:* Lighthouse or `axe-core`.
    *   *Target:* No critical WCAG 2.1 AA violations.

### B. Documentation Updates
*   [ ] **Project Plan Update:** Mark all items in `docs/project-plan.md` as `[x]`. Add "Closure" phase.
*   [ ] **README.md Refinement:**
    *   Ensure "Getting Started" instructions are flawless for a fresh clone.
    *   Verify prerequisites (Node version, Python version, Docker if applicable).
*   [ ] **Workflow & Architecture:**
    *   Ensure `docs/architecture.md` reflects the final state (e.g., any deviations during implementation).
    *   Verify `docs/bmm-workflow-status.yaml` is up to date.

### C. Release & Submission Prep
*   [ ] **Clean Up:** Remove any temporary test files, debug logs, or `.env` files containing actual secrets (ensure `.env.example` is valid).
*   [ ] **Tagging:** Create a git tag for the submission version.
    *   *Tag:* `v1.0.0-submission`
*   [ ] **Submission Checklist:**
    *   Repository is clean.
    *   Video/Demo link (if required) is in README.
    *   Final "Definition of Done" check.

## 3. Definition of Done (Project Completion)
The project is considered "Done" when:
1.  **Codebase:** All MVP features (Upload, OCR, Summary, Quiz, Auth) are implemented and merged to `main`.
2.  **Quality:**
    *   Unit tests pass.
    *   Critical E2E flows pass.
    *   Known bugs/skips are explicitly documented in `docs/known-issues.md` or `README.md`.
3.  **Documentation:**
    *   Full architectural documentation exists.
    *   User Guide (or usage instructions) is clear.
    *   Sprint artifacts (Retrospectives, Plans) are present in `docs/`.
4.  **Compliance:** No sensitive keys in version control.

## 4. Known Issues / Skips
*   **Dashboard Test:** Currently skipped due to [specific reason, e.g., flakiness or mock data issue]. documented in `tests/README.md`.
*   **RAG/Vector DB:** Explicitly out of scope for this MVP (as noted in PRD).
