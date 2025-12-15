# Story 5.1: Flashcard Review

**As a user, I want to be able to review my generated flashcards, so that I can study the material.**

## Acceptance Criteria

*   Given I have generated flashcards for a document,
*   When I navigate to the flashcard review page for that document,
*   Then I am presented with the first flashcard, showing the question.
*   And I can click a "Flip" button to reveal the answer.
*   And I can click "I knew it" or "I didn't know it" to move to the next card.
*   And the system keeps track of my progress in the session.
*   When I have reviewed all the cards,
*   Then I am shown a summary of the session (e.g., "You knew 8 out of 10 cards").

## Technical Tasks

### Backend

1.  **Create API Endpoint:**
    *   `GET /api/documents/{document_id}/flashcards`
    *   **Description:** Fetches all flashcards associated with a specific document.
    *   **Auth:** Must be protected, user can only access their own document's flashcards.
    *   **Response:** A JSON array of flashcard objects, each with a `question` and `answer` field.
    *   **Model:**
        ```python
        from pydantic import BaseModel

        class Flashcard(BaseModel):
            id: int
            question: str
            answer: str
        ```

2.  **Database:**
    *   Ensure the `flashcards` table has a foreign key to the `documents` table.

### Frontend

1.  **Create Page Component:**
    *   `src/pages/review/[id].tsx`
    *   **Description:** This will be the main page for a flashcard review session. The `[id]` will be the document ID.
    *   **Data Fetching:** Use `getServerSideProps` or a client-side fetch (e.g., with `useSWR` or `react-query`) to get the flashcards from the `/api/documents/{id}/flashcards` endpoint.

2.  **Create `Flashcard` Component:**
    *   `src/components/Flashcard.tsx`
    *   **Props:** `question: string`, `answer: string`, `isFlipped: boolean`, `onFlip: () => void`.
    *   **Functionality:**
        *   Displays the question by default.
        *   When `isFlipped` is true, it shows the answer.
        *   The `onFlip` function will be called when the user clicks a "Flip" button.

3.  **State Management:**
    *   Use `useState` or a state management library (Zustand/Context API) in the `[id].tsx` page to manage:
        *   `currentCardIndex`: The index of the card being displayed.
        *   `isFlipped`: Whether the current card is flipped or not.
        *   `knownCount`: The number of cards the user has marked as "known".
        *   `sessionComplete`: A boolean to track if the session is over.

4.  **UI/UX:**
    *   A clear "Flip" button on the flashcard.
    *   Two buttons below the card: "I knew it" (green) and "I didn't know it" (red).
    *   A progress indicator (e.g., "Card 3 of 10").
    *   When the session is complete, display a summary screen with the results and a button to return to the dashboard.
