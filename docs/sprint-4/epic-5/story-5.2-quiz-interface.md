# Story 5.2: Quiz Interface

**As a user, I want to be able to take the generated quiz, so that I can assess my understanding.**

## Acceptance Criteria

*   Given I have generated a quiz for a document,
*   When I navigate to the quiz page for that document,
*   Then I am presented with the first question and its multiple-choice options.
*   And I can select one answer for the current question.
*   And I can navigate to the next or previous question.
*   And my selected answers are saved as I navigate.
*   When I am on the last question,
*   Then the "Next" button becomes a "Submit" button.
*   When I click "Submit",
*   Then my answers are sent to the backend for grading.

## Technical Tasks

### Backend

1.  **Create API Endpoint for Fetching Quiz:**
    *   `GET /api/documents/{document_id}/quiz`
    *   **Description:** Fetches the quiz (questions and choices) for a specific document.
    *   **Auth:** Must be protected.
    *   **Response:** A JSON object containing the quiz ID and a list of questions. Each question should have an ID, the question text, and a list of choices (without revealing the correct answer).
    *   **Model:**
        ```python
        from pydantic import BaseModel
        from typing import List

        class QuizChoice(BaseModel):
            id: int
            text: str

        class QuizQuestion(BaseModel):
            id: int
            text: str
            choices: List[QuizChoice]

        class Quiz(BaseModel):
            id: int
            questions: List[QuizQuestion]
        ```

### Frontend

1.  **Create Page Component:**
    *   `src/pages/quiz/[id].tsx`
    *   **Description:** The main page for taking a quiz. The `[id]` will be the document ID, which is used to fetch the quiz.
    *   **Data Fetching:** Fetch the quiz data from the `/api/documents/{id}/quiz` endpoint.

2.  **Create `Question` Component:**
    *   `src/components/Question.tsx`
    *   **Props:** `question: QuizQuestion`, `selectedAnswer: number | null`, `onAnswerSelect: (choiceId: number) => void`.
    *   **Functionality:**
        *   Displays the question text.
        *   Displays the multiple-choice options as radio buttons or a clickable list.
        *   Highlights the `selectedAnswer` if one has been chosen.
        *   Calls `onAnswerSelect` when the user chooses an answer.

3.  **State Management:**
    *   Use state management in `[id].tsx` to handle:
        *   `quizData`: The fetched quiz questions and choices.
        *   `currentQuestionIndex`: The index of the currently displayed question.
        *   `userAnswers`: An object or map to store the user's selected choice ID for each question ID (e.g., `{ questionId_1: choiceId_3, ... }`).

4.  **Navigation:**
    *   Implement "Next" and "Previous" buttons.
    *   The "Next" button should be disabled if no answer is selected for the current question (optional, based on UX preference).
    *   The "Previous" button should be hidden or disabled on the first question.
    *   The "Next" button's text should change to "Submit" on the last question.

5.  **Submission:**
    *   When the "Submit" button is clicked, make a `POST` request to the `/api/quizzes/{quiz_id}/submit` endpoint (to be defined in Story 5.3).
    *   The request body should contain the `userAnswers` object.
    *   After submission, redirect the user to the results page (e.g., `/results/{quiz_id}`).
