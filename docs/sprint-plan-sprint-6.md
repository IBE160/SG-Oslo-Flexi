# Sprint Plan: Sprint 6 (Epic 7: QA & UX Excellence)

**Sprint Goal:** Achieve full WCAG 2.1 Level AA accessibility compliance across the core user journey, ensuring AI Buddy is usable by everyone, including users relying on assistive technologies.

## 1. Scope & Objectives

*   **Primary Focus:** Epic 7, Story 7.1 (Accessibility Compliance).
*   **Secondary Focus:** None (Dedicated Quality Sprint).
*   **In-Scope Story:**
    *   **Story 7.1:** Accessibility Compliance (WCAG 2.1 AA) - *As a user with disabilities, I want the application to be accessible and navigable using assistive technologies...*

## 2. Task Breakdown (Story 7.1)

To achieve the goal, we will break Story 7.1 down into the following actionable technical tasks:

### T1: Automated Accessibility Testing Setup
*   **Description:** Integrate `axe-core` (via `playwright-axe` or similar) into the existing Playwright E2E test suite.
*   **Output:** A base test fixture that runs accessibility checks on every visited page.

### T2: Global Accessibility Audit & Base Fixes
*   **Description:** Audit global styles and layout components (Navbar, Footer, Layout wrapper). Fix high-impact issues:
    *   Color contrast ratios (text vs background).
    *   Missing `alt` attributes on generic images/logos.
    *   Global focus ring visibility (ensure `outline-none` is replaced with visible focus indicators for keyboard users).
    *   Semantic HTML structure (main, nav, header, footer usage).

### T3: Auth & Onboarding Flow Accessibility
*   **Description:** Remediation for Login, Register, and Onboarding pages.
    *   Ensure form labels are correctly associated with inputs (`for` / `id`).
    *   Error messages must be programmatically associated with inputs (using `aria-describedby`).
    *   Keyboard navigation order check.

### T4: Dashboard & File Upload Accessibility
*   **Description:** Remediation for the main Dashboard and File Upload component.
    *   File upload dropzone must be keyboard accessible (enter to open file dialog).
    *   Status messages (uploading, processing) must use `aria-live` regions to announce changes to screen readers.
    *   Interactive cards (previous quizzes) must have proper button/link roles.

### T5: Learning Interface Accessibility (Critical)
*   **Description:** Remediation for Quiz and Flashcard interfaces.
    *   **Flashcards:** Ensure the "flip" action is keyboard accessible and the content of the back side is readable by screen readers only when revealed (or managed via `aria-hidden`).
    *   **Quiz:** Radio buttons/options must be grouped (`fieldset`, `legend`).
    *   Timer/Progress indicators must be accessible (e.g., proper ARIA roles).

### T6: Manual Keyboard & Screen Reader Validation
*   **Description:** Manual pass through the entire app using *only* the keyboard (Tab, Enter, Space, Esc).
*   **Optional:** Basic validation with a screen reader (e.g., NVDA or VoiceOver) if environment permits, or simulating via tools.

## 3. Dependencies

*   **Existing Codebase:** Access to Frontend (`frontend/`) repository.
*   **Tools:** `playwright`, `@axe-core/playwright`.
*   **Design Specs:** Reference to `ux-color-themes.html` for approved color palettes (checking against contrast requirements).

## 4. Risks & Mitigations

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Complex Interactive Components** | Flashcards and custom file uploaders may be hard to make fully accessible without breaking design/UX. | Research accessible patterns (WAI-ARIA Authoring Practices) before refactoring. Use standard HTML elements where possible. |
| **Contrast Color Changes** | Changing colors for contrast might clash with the brand aesthetic defined in `ux-design-directions.html`. | Consult UX Guidelines. Tweaking shades slightly (e.g., darker blue) usually suffices without breaking branding. |
| **"Over-engineering" ARIA** | Adding too many ARIA attributes can actually make the experience worse. | Stick to "First Rule of ARIA": Use native HTML elements (button, input, label) first. Use ARIA only when necessary. |

## 5. Acceptance Criteria & Definition of Done

### For Story 7.1:
*   [ ] **Automated Checks:** All pages pass `axe-core` checks with 0 "Critical" or "Serious" violations.
*   [ ] **Keyboard Nav:** Full user journey (Login -> Upload -> Quiz -> Result) can be completed using *only* the keyboard.
*   [ ] **Visual Focus:** All interactive elements have a clearly visible focus state.
*   [ ] **Forms:** All form inputs have associated labels and accessible error states.
*   [ ] **Contrast:** Text contrast ratios meet WCAG AA standards (4.5:1 for normal text).

### Definition of Done (Sprint Level):
*   Code refactored and committed to `main` (or feature branch).
*   Automated accessibility tests added to CI pipeline.
*   Validation Report created (`validation-report-story-7.1.md`) documenting the "Before" vs "After" state (e.g., screenshot of axe audit results).

## 6. Execution Order

1.  **T1:** Setup Testing Infrastructure (Fail first).
2.  **T2:** Fix Global Basics (Contrast, Focus, Structure).
3.  **T3:** Fix Auth Forms.
4.  **T4:** Fix Dashboard & Upload (High user impact).
5.  **T5:** Fix Complex Learning UI (Quiz/Flashcards).
6.  **T6:** Final Verification & Report.
