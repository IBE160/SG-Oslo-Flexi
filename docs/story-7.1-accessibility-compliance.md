# Story 7.1: Accessibility Compliance (WCAG 2.1 AA)

**Epic:** Epic 7: Quality Assurance & UX Excellence  
**Story Status:** In Progress  
**Sprint:** Sprint 6

## 1. User Story

**As a** user with disabilities (e.g., visual impairment, motor difficulty),  
**I want** the AI Buddy application to be accessible and navigable using assistive technologies (keyboard, screen reader),  
**So that** I can effectively use the tool to study without barriers.

## 2. Scope

This story covers the remediation of the entire core user journey to meet **WCAG 2.1 Level AA** standards.

**Included Flows:**
1.  **Global UI:** Navigation, Footer, Layout structure, Colors, Focus states.
2.  **Authentication:** Login and Registration forms (labels, errors, keyboard nav).
3.  **Dashboard:** Main dashboard layout, file upload dropzone.
4.  **Learning Interface:**
    *   **Flashcards:** Flipping mechanism, content visibility to screen readers.
    *   **Quiz:** Selection of answers, submission, result feedback.

**Out of Scope:**
*   Administrative interfaces (if any).
*   PDF document accessibility (we control the app UI, not the user's uploaded content, though our *output* must be accessible).

## 3. Functional Requirements (FRs)

*   **FR 7.1.1:** All text content MUST meet a minimum contrast ratio of 4.5:1 against its background (3:1 for large text).
*   **FR 7.1.2:** All interactive elements (buttons, links, inputs) MUST be navigable via keyboard (Tab, Enter, Space, Esc).
*   **FR 7.1.3:** All interactive elements MUST have a clearly visible focus indicator when focused.
*   **FR 7.1.4:** All form inputs MUST have programmatically associated labels.
*   **FR 7.1.5:** Dynamic content changes (e.g., "Processing...", "Correct!") MUST be announced to screen readers via `aria-live`.
*   **FR 7.1.6:** Images MUST have appropriate `alt` text (or be hidden if decorative).

## 4. Technical Constraints & Standards

*   **Standard:** WCAG 2.1 Level AA.
*   **Testing Tool:** `axe-core` (via Playwright) for automated checks.
*   **Manual Testing:** Keyboard-only navigation check is mandatory.
*   **Framework:** Next.js (React). Use semantic HTML (`<button>`, `<nav>`, `<h1>`) over `<div>` soup.
*   **Styling:** Tailwind CSS. Use specific utility classes for focus (`focus:ring`, `focus:outline-none`) and screen-reader only text (`sr-only`).

## 5. Acceptance Criteria

*   **AC 1: Automated Audit Pass**
    *   Given the Playwright accessibility test suite is run,
    *   When scanning Landing, Login, Register, Dashboard, and Quiz pages,
    *   Then `axe-core` SHALL report **0 violations** of "critical" or "serious" impact.

*   **AC 2: Keyboard Navigation**
    *   Given I am a keyboard-only user,
    *   When I navigate from Login -> Upload -> Quiz,
    *   Then I can access and activate every control using only `Tab`, `Shift+Tab`, `Enter`, and `Space`.
    *   And I never get "trapped" in a component.
    *   And I can always see which element has focus (visible ring).

*   **AC 3: Screen Reader Support (Forms)**
    *   Given I am using a screen reader (or inspection tool),
    *   When I focus on any input field (Email, Password),
    *   Then the label is announced.
    *   And if there is an error, the error message is announced immediately.

*   **AC 4: Interactive Components (Flashcards/Quiz)**
    *   Given I am reviewing flashcards,
    *   When I "flip" a card using the keyboard,
    *   Then the content of the new side is revealed to the screen reader.
    *   Given I am taking a quiz,
    *   When I select an answer and submit,
    *   Then the result ("Correct/Incorrect") is announced without moving focus manually.

## 6. Task Breakdown (Sprint 6)

1.  **T1: Automated Accessibility Testing Setup** (Completed)
    *   Install `@axe-core/playwright`.
    *   Create `tests/e2e/a11y.spec.ts`.
    *   Integrate into CI.

2.  **T2: Global Accessibility Audit & Base Fixes**
    *   Update Tailwind config for colors if needed.
    *   Add global focus ring styles to `globals.css`.
    *   Fix "Skip to Content" link and semantic landmarks (`main`, `nav`, `footer`).
    *   Fix contrast issues on Landing page buttons/text.

3.  **T3: Auth & Onboarding Flow Accessibility**
    *   Add `<label>` or `aria-label` to Login/Register inputs.
    *   Link error messages with `aria-describedby`.
    *   Ensure contrast on link text.

4.  **T4: Dashboard & File Upload Accessibility**
    *   Make the file dropzone keyboard accessible (button to open file dialog).
    *   Add `aria-live` region for "Uploading..." status.

5.  **T5: Learning Interface Accessibility (Critical)**
    *   Refactor Flashcard component: Use `button`, manage `aria-pressed`/`aria-hidden` for sides.
    *   Refactor Quiz component: Use `fieldset`/`legend` for question grouping.
    *   Add live region for Quiz feedback.

6.  **T6: Final Verification**
    *   Run full manual keyboard pass.
    *   Verify CI checks pass green.

## 7. Definition of Done

*   [ ] Code changes merged to `main`.
*   [ ] `tests/e2e/a11y.spec.ts` passes in CI.
*   [ ] Manual validation checklist completed and signed off in `validation-report-story-7.1.md`.
