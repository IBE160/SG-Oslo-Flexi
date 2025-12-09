# Story 2.3: Basic Onboarding

**Status:** done

## Story

**As a new user,** I want to be guided through the core features of the application immediately after my first login, so that I can quickly understand how to upload documents and generate quizzes without confusion.

## Acceptance Criteria

*   **AC1:** Given I have just registered and logged in for the first time,
    *   Then I am presented with an "Onboarding Wizard" (e.g., a modal or overlay).
*   **AC2:** The onboarding wizard must guide me through:
    1.  **Welcome:** A brief welcome message.
    2.  **Upload:** Highlighting the "Document Upload" feature.
    3.  **Generate:** Highlighting the "Generate Quiz" feature.
*   **AC3:** When I complete or dismiss the onboarding wizard,
    *   Then my user profile is marked as `onboarded`.
    *   And I am not shown the wizard on subsequent logins.
*   **AC4:** If I have already completed onboarding,
    *   Then I am taken directly to the dashboard upon login without seeing the wizard.

## Dev Notes

### References

*   [Source: docs/epics.md#epic-2-user-authentication--onboarding]
*   [Source: docs/tech-spec-epic-2.md#story-23-basic-onboarding]

### Architecture patterns and constraints

*   **Persistence:** The onboarding state must be stored in the database (`users` table) to persist across sessions and devices. Do not rely solely on local storage.
*   **Frontend-Backend Sync:** The frontend session (NextAuth) needs to be aware of the `is_onboarded` status to conditionally render the wizard.
*   **UX:** The wizard should be unobtrusive but clear. Standard modal or "tour" libraries can be considered, or a custom simple implementation.

## Tasks

### Backend

*   [x] (AC: #3) **Model Update:** Add `is_onboarded` (boolean, default `false`) to the `User` model.
*   [x] (AC: #3) **Schema Update:** Update `UserRead` schema to include `is_onboarded`.
*   [x] (AC: #3) **Migration:** Create and apply Alembic migration for the `users` table change.
*   [x] (AC: #3) **Endpoint:** Create `POST /api/v1/users/onboarding` (or similar) to update the status to `true`.
*   [x] (AC: #3) **Testing:** Verify the status update persists and is returned in user details.

### Frontend

*   [x] (AC: #1, #4) **Session:** Update NextAuth session types to include `is_onboarded`.
*   [x] (AC: #2) **Component:** Create `OnboardingWizard` component (UI for Welcome -> Upload -> Generate).
*   [x] (AC: #3) **Service:** Add API call `completeOnboarding` to the frontend service layer.
*   [x] (AC: #1, #4) **Integration:** In the main Dashboard/Layout, check `user.is_onboarded`. If false, mount `OnboardingWizard`.
*   [x] (AC: #3) **Logic:** On wizard completion, call API and locally update session/state to close wizard.

## Dev Agent Record

*   **Context Reference:** Story 2.3 Definition
*   **Agent Model Used:** N/A (Planning Phase)
*   **Debug Log References:** N/A
*   **Completion Notes List:** N/A
*   **File List:** N/A

## Change Log

*   2025-12-09: Initial story definition created by SM Agent.
