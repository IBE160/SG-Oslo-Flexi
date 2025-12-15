# Technical Specification: Epic 7 (Quality Assurance & UX Excellence)

## 1. Introduction

This technical specification defines the standards, tools, and implementation details for achieving **Accessibility Compliance (WCAG 2.1 Level AA)** across the AI Buddy application. This focus ensures that the platform is usable by people with disabilities, including those using screen readers, keyboard-only navigation, and other assistive technologies.

**Scope:** This specification covers the entire frontend application (Next.js), specifically focusing on the core user flows: Authentication, Dashboard/Upload, and the Learning Interface (Quiz/Flashcards).

## 2. Standards & Requirements

We target **WCAG 2.1 Level AA** compliance. Key success criteria include:

*   **1.4.3 Contrast (Minimum):** Text has a contrast ratio of at least 4.5:1 (large text 3:1).
*   **2.1.1 Keyboard:** All functionality is available from a keyboard.
*   **2.4.3 Focus Order:** Focusable components receive focus in an order that preserves meaning and operability.
*   **2.4.7 Focus Visible:** Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible.
*   **1.1.1 Non-text Content:** All non-text content (images) has a text alternative (alt text).
*   **3.3.1 Error Identification:** If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text.
*   **4.1.2 Name, Role, Value:** User interface components (buttons, links, inputs) have a name, role, and value that can be programmatically determined.

## 3. Tooling & Testing Strategy

### 3.1. Automated Testing (CI/CD)

We will integrate `axe-core` into our existing Playwright E2E test suite to catch common accessibility violations automatically.

*   **Library:** `@axe-core/playwright`
*   **Integration:**
    *   Create a custom Playwright fixture or helper function (e.g., `checkA11y(page)`) that injects and runs `axe` on the current page state.
    *   Configure `axe` to assert 0 violations for "critical" and "serious" impact issues.
    *   Run these tests as part of the `CI` workflow on every pull request.

**Example Playwright Test Snippet:**

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('landing page should not have any automatically detectable accessibility issues', async ({ page }) => {
  await page.goto('/');
  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### 3.2. Manual Validation

Automated tools only catch ~30-50% of issues. Manual testing is mandatory.

*   **Keyboard Navigation:** Tab through every interactive element. Ensure logical order and visible focus rings. Check that `Enter` and `Space` activate buttons/links. Verify `Esc` closes modals.
*   **Screen Reader (Simulation):** Use tools like **NVDA** (Windows), **VoiceOver** (macOS), or Chrome's **Screen Reader** extension to verify that:
    *   Images have meaningful descriptions.
    *   Form labels are announced correctly.
    *   Dynamic content updates (e.g., "Processing...", "Correct Answer") are announced via `aria-live`.

## 4. Implementation Guidelines

### 4.1. Semantic HTML & Structure

*   Use semantic tags (`<nav>`, `<main>`, `<header>`, `<footer>`, `<article>`, `<aside>`) to define page structure.
*   **Headings:** Ensure a logical heading hierarchy (`h1` -> `h2` -> `h3`). Do not skip levels (e.g., `h1` to `h3`).
*   **Buttons vs. Links:**
    *   Use `<button>` for actions (e.g., "Submit", "Open Menu", "Flip Card").
    *   Use `<a>` (via Next.js `<Link>`) for navigation (changing the URL).
    *   *Never* use `div` or `span` with `onClick` without adding `role="button"` and keyboard handlers (but prefer native elements).

### 4.2. Focus Management

*   **Visible Focus:**
    *   **Do not** remove default outlines (`outline: none`) without replacing them with a custom focus style (e.g., `ring-2 ring-blue-500`).
    *   Ensure focus contrast is sufficient.
*   **Skip Links:** Implement a "Skip to Main Content" link as the first focusable element on the page.
*   **Modals:** When a modal opens, focus must move *into* the modal. When it closes, focus must return to the trigger element. Trap focus inside the modal while open.

### 4.3. Color & Contrast

*   **Text:** Verify all text meets 4.5:1 contrast against its background.
    *   *Caution:* Light gray text on white backgrounds often fails.
    *   *Caution:* Text over images requires a scrim or solid background.
*   **UI Components:** Borders of inputs and buttons should also have sufficient contrast (3:1) against the page background to be identifiable.
*   **Color Independence:** Do not rely on color alone to convey meaning (e.g., use an icon *and* red color for error messages).

### 4.4. Forms & Error Handling

*   **Labels:** Every input **must** have a label.
    *   Visible labels: `<label for="email">Email</label><input id="email" ... />`.
    *   Hidden labels (if visually redundant but needed for a11y): Use `aria-label` or a visually hidden class.
*   **Errors:**
    *   Associate error messages with inputs using `aria-describedby`.
    *   Example: `<input aria-describedby="email-error" ... /> <span id="email-error">Invalid email</span>`.

### 4.5. Interactive Components (Quiz & Flashcards)

#### Flashcards
*   **Structure:** The card container should likely be a `<button>` (or have `role="button"`).
*   **State:** Use `aria-pressed` or `aria-expanded` to indicate the "flipped" state if applicable, or manage content visibility.
*   **Screen Readers:** Ensure the "back" content is hidden from screen readers (`aria-hidden="true"`) when the card is face up, and vice-versa, OR ensure the focus moves to the new content when revealed.

#### Quiz Interface
*   **Selection:** Use standard `<input type="radio">` grouped in a `<fieldset>` with a `<legend>` for the question text. This ensures the question is announced when an option is selected.
*   **Feedback:** When an answer is submitted, the result ("Correct/Incorrect") should be announced immediately. Use a live region: `<div aria-live="polite">Correct!</div>`.

## 5. Remediation Plan (Execution Order)

1.  **Global:** Update `tailwind.config.ts` (or CSS variables) to ensure default color palette meets contrast standards. Add global focus ring styles.
2.  **Layout:** Add "Skip to Content" link. Fix semantic structure of `Layout.tsx`.
3.  **Components:** Audit and fix reusable components: `Button`, `Input`, `Card`, `Modal`.
4.  **Pages:**
    *   **Auth:** Fix form labels and error associations.
    *   **Dashboard:** Fix keyboard nav for file upload dropzone.
    *   **Quiz/Flashcards:** Refactor for semantic HTML and ARIA roles.

## 6. Definition of Done (Story 7.1)

*   [ ] All critical flows pass `axe-core` automated checks (0 violations).
*   [ ] Manual keyboard navigation confirms full operability without mouse.
*   [ ] Interactive elements have visible focus states.
*   [ ] Screen reader validation confirms content is announced logically.
*   [ ] Code review confirms use of semantic HTML and proper ARIA attributes.
