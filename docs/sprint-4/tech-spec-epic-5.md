# Epic 5: Learning & Assessment - Technical Specification

**Goal:** Create the user-facing learning experience, including the quiz interface, flashcard review, and results display.

---

## Story 5.1: Flashcard Review

**As a user, I want to be able to review my generated flashcards, so that I can study the material.**

### Acceptance Criteria:

*   Given I have generated flashcards,
*   When I start a review session,
*   Then I am shown one flashcard at a time, with the ability to flip it and mark it as "known" or "unknown".

### Technical Breakdown:

*   **Frontend:**
    *   Create a new page component `FlashcardReview.tsx` under `/src/pages/review/[id].tsx`.
    *   This page will fetch the flashcard data from the backend using the document ID.
    *   Implement a state management solution (e.g., React Context or Zustand) to manage the flashcard session (current card index, user answers).
    *   Create a `Flashcard` component that displays a single flashcard with a front (question) and back (answer).
    *   Add a "Flip" button to toggle between the front and back of the flashcard.
    *   Add "Known" and "Unknown" buttons to allow the user to self-assess their knowledge.
    *   Implement the logic to cycle through the flashcards.
*   **Backend:**
    *   Create a new API endpoint `GET /api/documents/{document_id}/flashcards` to fetch the generated flashcards for a specific document.
    *   This endpoint should return the flashcards associated with the document from the database.
    *   Ensure the endpoint is protected and that the user can only access their own documents.

---

## Story 5.2: Quiz Interface

**As a user, I want to be able to take the generated quiz, so that I can assess my understanding.**

### Acceptance Criteria:

*   Given I have generated a quiz,
*   When I start the quiz,
*   Then I am presented with one question at a time, with multiple-choice options.

### Technical Breakdown:

*   **Frontend:**
    *   Create a new page component `Quiz.tsx` under `/src/pages/quiz/[id].tsx`.
    *   This page will fetch the quiz data from the backend using the document ID.
    *   Implement state management to track the quiz progress (current question index, user answers).
    *   Create a `Question` component that displays a single quiz question and its multiple-choice options.
    *   Implement the logic to record the user's selected answer for each question.
    *   Add "Next" and "Previous" buttons to navigate between questions.
    *   Add a "Submit" button at the end of the quiz.
*   **Backend:**
    *   Create a new API endpoint `GET /api/documents/{document_id}/quiz` to fetch the generated quiz for a specific document.
    *   This endpoint should return the quiz questions and options from the database.
    *   Ensure the endpoint is protected and that the user can only access their own documents.

---

## Story 5.3: Quiz Results

**As a user, I want to see my quiz results after completing a quiz, so that I can understand my performance.**

### Acceptance Criteria:

*   Given I have completed a quiz,
*   When I submit my answers,
*   Then I am shown my score and a breakdown of which questions I answered correctly and incorrectly.

### Technical Breakdown:

*   **Frontend:**
    *   Create a new page component `QuizResults.tsx` under `/src/pages/results/[id].tsx`.
    *   This page will be displayed after the user submits a quiz.
    *   It will display the user's score (e.g., "You scored 4 out of 5").
    *   It will also display a list of the questions, the user's answer, and the correct answer, highlighting the correct and incorrect answers.
    *   Add a "Back to Dashboard" button.
*   **Backend:**
    *   Create a new API endpoint `POST /api/quizzes/{quiz_id}/submit` to submit the user's answers.
    *   This endpoint will receive the user's answers and calculate the score.
    *   It will store the quiz results in the database, associated with the user and the quiz.
    *   The endpoint will return the quiz results, including the score and the correct answers for each question.
    *   Create a new database table `quiz_results` to store the results of each quiz taken by a user. This table should include columns for `user_id`, `quiz_id`, `score`, and the user's answers.

---
