# Story 5.3: Quiz Results

**As a user, I want to see my quiz results after completing a quiz, so that I can understand my performance.**

## Acceptance Criteria

*   Given I have submitted a quiz,
*   When the submission is processed,
*   Then I am redirected to a results page.
*   And the results page displays my overall score (e.g., "4/5" or "80%").
*   And the page shows a breakdown of each question.
*   For each question, it clearly indicates the answer I chose and whether it was correct or incorrect.
*   And the correct answer is always shown.

## Technical Tasks

### Backend

1.  **Create API Endpoint for Submission:**
    *   `POST /api/quizzes/{quiz_id}/submit`
    *   **Description:** Receives the user's answers, calculates the score, saves the result, and returns the graded results.
    *   **Auth:** Must be protected.
    *   **Request Body:**
        ```json
        {
          "answers": {
            "question_id_1": "choice_id_2",
            "question_id_2": "choice_id_4",
            ...
          }
        }
        ```
    *   **Logic:**
        1.  Retrieve the quiz and its questions/correct answers from the database using the `quiz_id`.
        2.  Iterate through the user's answers and compare them to the correct answers.
        3.  Calculate the final score.
        4.  Create a new record in the `quiz_results` table.
        5.  Return the detailed results.
    *   **Response Body:**
        ```json
        {
          "result_id": "new_result_id",
          "score": 0.8,
          "results": [
            {
              "question_id": "question_id_1",
              "question_text": "What is 2+2?",
              "your_answer_id": "choice_id_2",
              "correct_answer_id": "choice_id_3",
              "is_correct": false
            },
            ...
          ]
        }
        ```

2.  **Create Database Table:**
    *   `quiz_results`
    *   **Columns:**
        *   `id` (Primary Key)
        *   `user_id` (Foreign Key to `users`)
        *   `quiz_id` (Foreign Key to `quizzes`)
        *   `score` (Float or Decimal)
        *   `submitted_at` (Timestamp)
    *   `quiz_answers` (or similar name)
    *   **Columns:**
        *   `id` (Primary Key)
        *   `result_id` (Foreign Key to `quiz_results`)
        *   `question_id` (Foreign Key to `questions`)
        *   `selected_choice_id` (Foreign Key to `choices`)


3.  **Create API Endpoint for Fetching Results:**
    *   `GET /api/results/{result_id}`
    *   **Description:** Fetches a previously saved quiz result.
    *   **Auth:** Must be protected; user can only fetch their own results.
    *   **Response:** The same detailed result format as the `POST` submission response.

### Frontend

1.  **Create Page Component:**
    *   `src/pages/results/[id].tsx`
    *   **Description:** Displays the results of a quiz. The `[id]` will be the `result_id` returned by the submission endpoint.
    *   **Data Fetching:** Fetch the result data from `/api/results/{id}`.

2.  **UI/UX:**
    *   A prominent display of the final score (e.g., in a large font or inside a chart).
    *   A list of questions. Each item in the list should contain:
        *   The question text.
        *   The user's answer, with a visual indicator (e.g., a red 'X' or green checkmark) showing if it was correct.
        *   The correct answer, clearly marked.
    *   A "Back to Dashboard" or "Try Again" button.
