# AI Buddy - UX Design Specification

## 1. Project Vision and Understanding

*   **Project:** AI Buddy is a web-based learning assistant that helps students study more effectively by using a multi-agent AI system to automatically generate summaries, flashcards, and quiz questions from uploaded study materials.
*   **Target Users:** University and college students, as well as self-learners and professionals.
*   **Core Experience:** Seamlessly uploading study materials and instantly receiving a "Learning Pack" of summaries, flashcards, and quizzes.
*   **Desired Feeling:** Efficient, productive, creative, inspired, calm, and focused.
*   **Platform:** A web application for both desktop and mobile.
*   **Inspiration:** The productivity of Notion, the focus of Quizlet, and the calmness of Headspace.

## 2. Design System and Visual Foundation

*   **Design System:** Shadcn UI
*   **Color Theme:** Focus (Monochromatic Blue)
    *   **Primary:** #0d6efd
    *   **Secondary:** #6c757d
    *   **Success:** #198754
    *   **Warning:** #ffc107
    *   **Error:** #dc3545
*   **Typography:** Default typography from Shadcn UI.
*   **Spacing and Layout:** Default spacing and layout from Shadcn UI.

## 3. Defining Experience and Core Principles

*   **Defining Experience:** "It's the app that instantly turns my messy notes into a focused study session."
*   **Core Experience Principles:**
    *   **Speed:** The transformation from messy notes to a focused study session should feel almost instant.
    *   **Guidance:** The user should always feel guided and supported, never lost or overwhelmed.
    *   **Flexibility:** The user should have control over their learning, with options to customize their study sessions.
    *   **Feedback:** The user should receive clear and immediate feedback on their progress and performance.

## 4. User Journeys

*   **First-Time Student Onboarding:**
    1.  **Entry:** The user is greeted with the "New Study Session" wizard. The first step, "Upload", is active.
    2.  **Input:** The user selects a file. The file name is displayed, and a "Continue" button becomes active.
    3.  **Feedback:** Upon clicking "Continue", the stepper moves to the "Process" step, with a loading indicator and friendly messages. When processing is complete, the stepper automatically moves to the "Study" step.
    4.  **Success:** The "Study" step presents the complete study set. The "Summary" is displayed by default, with clear tabs to switch to "Flashcards" and "Quiz". After completing the quiz, the stepper moves to the "Results" step.

*   **Returning User Dashboard (History):**
    *   **Context:** User logs in and wants to see past progress or review old materials (satisfies Epic 6).
    *   **Entry:** "Dashboard" or "My History" link in the top navigation.
    *   **View:** Simple list or table of "Recent Study Sessions".
    *   **Data Columns:**
        *   Document Name (e.g., "History_Lecture_101.pdf")
        *   Date Created (e.g., "Nov 26, 2025")
        *   Quiz Score (e.g., "4/5" or "-")
        *   Actions (Buttons: "Review Summary", "Retake Quiz")
    *   **Interactions:**
        *   Clicking "Retake Quiz" re-opens the Quiz Interface with the saved questions.
        *   Clicking "Review Summary" opens the Summary tab for that document.
    *   **Empty State:** If no history exists, show a friendly "Welcome back! Start your first study session" CTA leading to the Upload Wizard.

### 4.1. Layout decision for MVP

For the IBE160 MVP, the primary interaction pattern will be the **Stepper Wizard** layout, guiding the user through the "Upload → Process → Study → Results" flow as described above. This focused, linear journey aligns with our core experience principles of speed and guidance for a first-time user.

The alternative layouts explored in `ux-design-directions.html`, such as the sidebar, top navigation, and card-based dashboard, are considered valuable explorations for future iterations or for a "returning user" experience, but they are not part of the initial MVP implementation.

## 5. Component Library

*   **From Shadcn UI:** Button, Card, Input, Alert, Tabs, Progress.
*   **Custom Components:**
    *   **Stepper:** Guides the user through the onboarding process (Upload -> Process -> Study -> Results).
    *   **File Uploader:** Drag-and-drop zone with file type validation and progress indication.

    ### 5.1. Flashcard Interface Specification
    *   **Purpose:** Facilitate active recall testing with a focus on speed and simplicity.
    *   **Data Structure:**
        ```typescript
        interface Flashcard {
          id: string;
          front: string; // Question/Term
          back: string;  // Answer/Definition
        }
        ```
    *   **Props:**
        *   `cards`: Flashcard[]
        *   `onComplete`: (results: { known: string[], unknown: string[] }) => void
    *   **Internal State:**
        *   `currentIndex`: number (0 to cards.length - 1)
        *   `isFlipped`: boolean (false = front, true = back)
        *   `stats`: { knownCount: number, unknownCount: number }
    *   **Interaction Pattern:**
        1.  **Default:** Show card front. Text centered.
        2.  **Action (Click/Tap):** Animate flip (CSS transform) to show back.
        3.  **Action (Rating):**
            *   "I know this" (Check icon / Right arrow key) -> Mark known, slide card right, advance to next.
            *   "Study again" (X icon / Left arrow key) -> Mark unknown, slide card left, advance to next.
        4.  **Completion:** Show summary card with "Restart" or "Finish" options.
    *   **Visual States:**
        *   *Front:* Clean typography, large font size.
        *   *Back:* Slightly smaller font, supportive color accent.
        *   *Transition:* Smooth 300ms flip animation.
    *   **Loading and Error States:** When a flashcard deck is being generated or loaded, show a spinner or skeleton card. If the deck fails to load or is empty, show an inline message with a clear CTA (e.g., “Generate flashcards from this document”) instead of an empty card.

    ### 5.2. Quiz Interface Specification
    *   **Purpose:** Assess knowledge retention with immediate feedback (gamified feel).
    *   **Data Structure:**
        ```typescript
        interface QuizQuestion {
          id: string;
          questionText: string;
          options: { id: string; text: string }[];
          correctOptionId: string;
          explanation: string; // Shown after answering
        }
        ```
    *   **Props:**
        *   `questions`: QuizQuestion[]
        *   `onQuizComplete`: (score: number, total: number) => void
    *   **Internal State:**
        *   `currentIndex`: number
        *   `selectedOption`: string | null
        *   `isAnswerRevealed`: boolean
        *   `score`: number
    *   **Interaction Pattern:**
        1.  **Question View:** Display question and 4 vertical option buttons.
        2.  **Selection:** User clicks an option.
            *   *Immediate Feedback:* Selected option highlights.
            *   *Reveal:* If correct -> Turn Green. If incorrect -> Turn Red and highlight correct option in Green.
            *   *Explanation:* Slide down "Why this is correct/incorrect" panel.
        3.  **Progression:** "Next Question" button appears (auto-focus).
        4.  **Completion:** Show "Quiz Results" card with score (e.g., "4/5 Correct") and confetti animation for high scores.
    *   **Visual States:**
        *   *Idle:* Options have neutral outline/background.
        *   *Hover:* Option background slightly darker/accented.
        *   *Correct:* Green border & background, Check icon.
        *   *Incorrect:* Red border & background, Shake animation, X icon.
        *   *Disabled:* Non-selected options fade out when answer is revealed.
    *   **Loading and Error States:** When quiz questions are loading, show a spinner and simple placeholder skeleton. If loading fails, show an inline error (“We couldn’t load your quiz”) with a “Try again” button, while still allowing the user to navigate back to the main study view.

## 6. UX Pattern Decisions

*   **Button Hierarchy:** Primary (solid), Secondary (outline), Destructive (red).
*   **Feedback Patterns:** Success (toast), Error (inline), Loading (spinner).
*   **Form Patterns:** Labels (above), Validation (on blur), Error Display (inline).
*   **Navigation Patterns:** Active State (background color and bold font), Back Button (browser history).
*   **Modal Patterns:**
    *   **Usage:** Critical confirmations (e.g., "Discard Study Session?") or focused tasks (e.g., "Login/Register").
    *   **Behavior:** Centered, backdrop blur, closes on 'Esc' or outside click (unless critical).
    *   **Focus:** Auto-focus first input or primary action. Trap focus within modal.
*   **Empty State Patterns:**
    *   **Usage:** When a list is empty (e.g., Dashboard History) or search yields no results.
    *   **Components:**
        1.  **Illustration/Icon:** Friendly, non-alarming visual (e.g., an empty folder or calm mascot).
        2.  **Message:** Clear statement (e.g., "No study sessions yet").
        3.  **Call to Action:** Direct button to fix the state (e.g., "Start New Session").

## 7. Responsive and Accessibility Strategy

*   **Responsive Design:**
    *   **Desktop:** Sidebar for navigation, multi-column layout.
    *   **Tablet:** Collapsed sidebar (hamburger menu), two-column layout.
    *   **Mobile:** Bottom navigation bar, single-column layout.
    *   **Breakpoints (aligning with Tailwind/Shadcn defaults):**
        *   **≤ 640px (Mobile):** Single-column layout, stacked content.
        *   **641–1024px (Tablet):** Two-column layout where possible, collapsible navigation.
        *   **> 1024px (Desktop):** Multi-column layout with persistent sidebar navigation.
*   **Accessibility:** WCAG 2.1 Level A.
    *   **Contrast:** Text and interactive elements use a minimum contrast ratio of 4.5:1 against their background.
    *   **Keyboard Navigation:** All interactive elements (buttons, links, tabs, flashcards, quiz options) can be operated with keyboard only (Tab, Shift+Tab, Enter, Space, Arrow keys where appropriate).
    *   **Focus Indicators:** A visible focus ring is always shown on the currently focused element, including within modals and the Stepper Wizard.
    *   **ARIA & Semantics:**
        *   Modals use appropriate dialog semantics and trap focus until closed.
        *   Toasts and alerts use aria-live so feedback is announced to assistive technologies.
        *   Quiz questions and flashcards use semantic headings/regions so screen readers can understand the current step or card.
