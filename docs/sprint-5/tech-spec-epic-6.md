# Epic 6: Basic Progress Tracking - Technical Specification

**Goal:** Implement the basic progress tracking features, allowing users to see their quiz history and scores.

---

## Story 6.1: Quiz History

**As a user, I want to be able to see a history of the quizzes I have taken, so that I can track my progress over time.**

### Acceptance Criteria:

*   Given I have taken at least one quiz,
*   When I navigate to my dashboard,
*   Then I can see a list of my past quizzes, with the date and score for each.

### Technical Breakdown:

*   **Frontend:**
    *   Create a new component `QuizHistory.tsx` in `/src/components/`.
    *   This component will fetch the quiz history data from the backend.
    *   It will display the data in a table or list format, showing the quiz title, score, and date.
    *   Update the main dashboard page (`/src/pages/dashboard.tsx` or similar) to include the `QuizHistory` component.
*   **Backend:**
    *   Create a new API endpoint `GET /api/users/me/quiz-history` to fetch the quiz history for the currently authenticated user.
    *   This endpoint will query the `quiz_results` table to get all the quiz results for the user.
    *   It should return a list of objects, each containing the quiz title, score, and the date the quiz was taken.
    *   Create a new service function in a `UserService` to handle the logic of fetching the quiz history.

---

## Story 6.2: Basic Progress Dashboard

**As a user, I want to have a simple dashboard that shows my overall progress, so that I can stay motivated.**

### Acceptance Criteria:

*   Given I have taken at least one quiz,
*   When I view my dashboard,
*   Then I can see a summary of my average quiz score and the number of quizzes I have completed.

### Technical Breakdown:

*   **Frontend:**
    *   Create a new component `ProgressSummary.tsx` in `/src/components/`.
    *   This component will fetch the progress summary data from the backend.
    *   It will display the average score and the total number of quizzes taken.
    *   Update the main dashboard page to include the `ProgressSummary` component.
*   **Backend:**
    *   Create a new API endpoint `GET /api/users/me/progress-summary`.
    *   This endpoint will calculate the average score and total quizzes taken from the `quiz_results` table for the current user.
    *   It should return an object containing `averageScore` and `totalQuizzes`.
    *   Add a new function to the `UserService` to handle this logic.

---
