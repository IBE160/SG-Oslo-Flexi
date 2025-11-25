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

### 4.1. Layout decision for MVP

For the IBE160 MVP, the primary interaction pattern will be the **Stepper Wizard** layout, guiding the user through the "Upload → Process → Study → Results" flow as described above. This focused, linear journey aligns with our core experience principles of speed and guidance for a first-time user.

The alternative layouts explored in `ux-design-directions.html`, such as the sidebar, top navigation, and card-based dashboard, are considered valuable explorations for future iterations or for a "returning user" experience, but they are not part of the initial MVP implementation.

## 5. Component Library

*   **From Shadcn UI:** Button, Card, Input, Alert, Tabs, Progress.
*   **Custom Components:**
    *   **Stepper:** Guides the user through the onboarding process.
    *   **File Uploader:** For dragging and dropping or selecting files.
    *   **Quiz Interface (Kahoot Style):** An engaging and interactive quiz experience.
    *   **Flashcard Interface (Kahoot Style):** A fast-paced and gamified flashcard experience.

## 6. UX Pattern Decisions

*   **Button Hierarchy:** Primary (solid), Secondary (outline), Destructive (red).
*   **Feedback Patterns:** Success (toast), Error (inline), Loading (spinner).
*   **Form Patterns:** Labels (above), Validation (on blur), Error Display (inline).
*   **Navigation Patterns:** Active State (background color and bold font), Back Button (browser history).

## 7. Responsive and Accessibility Strategy

*   **Responsive Design:**
    *   **Desktop:** Sidebar for navigation, multi-column layout.
    *   **Tablet:** Collapsed sidebar (hamburger menu), two-column layout.
    *   **Mobile:** Bottom navigation bar, single-column layout.
*   **Accessibility:** WCAG 2.1 Level A.
