# Brainstorm – Quiz Engine (2025-11-09)

- **Must-haves (MVP)**
    - Generate a fixed-length quiz (e.g., 5 questions) from the document context provided by the OCR pipeline.
    - Questions must be exclusively Multiple-Choice Questions (MCQ) for the MVP.
    - Each MCQ must contain one verifiably correct answer and at least three plausible but incorrect distractors.
    - All generated content (questions, answers, distractors) must be directly derived from the source document text.
    - The entire quiz is generated in a single, atomic transaction and returned as a structured JSON object.

- **Should-haves (next)**
    - Introduce True/False (T/F) as an additional item type.
    - Allow the user to configure the length of the quiz.
    - Implement a mechanism to control and vary question difficulty (e.g., "conceptual" vs. "factual recall").
    - Add a post-generation check to filter out semantically duplicate questions.
    - Store quiz results and user performance over time.

- **Item types (MCQ, T/F) and minimal JSON schema**
    - The quiz will be represented as a JSON object containing an array of question "items".

    ```json
    {
      "quizId": "uuid-goes-here",
      "documentId": "source-document-uuid",
      "items": [
        {
          "itemType": "MCQ",
          "question": "What is the primary function of the mitochondria?",
          "options": [
            "To store genetic information",
            "To generate cellular energy (ATP)",
            "To synthesize proteins",
            "To facilitate cell division"
          ],
          "correctAnswerIndex": 1
        },
        {
          "itemType": "T/F",
          "question": "The Earth is the fourth planet from the Sun.",
          "correctAnswer": false
        }
      ]
    }
    ```

- **Scoring model (per item, total, pass rule)**
    - **Per item:** Binary scoring. Correct answer = 1 point. Incorrect answer = 0 points.
    - **Total:** Simple sum of points awarded for all items.
    - **Pass rule:** No strict "pass/fail" for the MVP. The final result is presented as a score (e.g., "You scored 4/5") and a percentage (80%).

- **UX flow (generate → answer → feedback → retry)**
    1.  **Generate:** User clicks a "Create Quiz" button. A loading animation is displayed while the engine generates the items.
    2.  **Answer:** The UI presents one question at a time. The user selects an answer and proceeds to the next question.
    3.  **Feedback:** Upon completion, a summary view displays the final score. It should list the questions and indicate which were answered correctly or incorrectly.
    4.  **Retry:** The user has an option to "Generate a new quiz" or return to the document.

- **Dependencies (Reader → Coach, storage)**
    - **Reader Agent:** The Quiz Engine is critically dependent on the clean, structured text output from the document OCR/parsing pipeline. Garbage in, garbage out.
    - **Coach Agent (LLM):** The engine is a specialized application of the LLM. Its performance is tied to the quality of the LLM and the sophistication of the prompt that instructs it to act as a quiz generator.
    - **Storage:** For the MVP, the engine is stateless. Quizzes are generated on-demand and not stored. State will be a "should-have" dependency.

- **Risks & mitigations (hallucinations, duplicates, difficulty, latency)**
    - **Risk: Hallucination:** LLM generates questions or answers not based on the source text.
        - **Mitigation:** Enforce a strict Retrieval-Augmented Generation (RAG) pattern. The generation prompt must explicitly forbid using outside knowledge and require grounding in the provided context.
    - **Risk: Duplicates:** The engine produces nearly identical questions.
        - **Mitigation:** Instruct the LLM in the prompt to ensure question diversity. A "should-have" is to add a post-processing step that uses embeddings to check for and filter out semantically similar questions.
    - **Risk: Difficulty:** Questions are consistently too easy or too hard.
        - **Mitigation:** Refine the prompt to ask for questions that test "understanding" rather than simple "search and find". For MVP, a consistent baseline difficulty is acceptable.
    - **Risk: Latency:** Quiz generation takes too long, creating a poor user experience.
        - **Mitigation:** Use an optimized LLM. The UX must clearly indicate that generation is in progress. Generate the entire quiz in one background request to avoid multiple chained LLM calls.

- **Proposed decision**
The MVP Quiz Engine will be a stateless service that, on request, uses a RAG-prompted LLM to generate a 5-item, MCQ-only quiz from a given text context. The entire quiz will be delivered in a single JSON payload to the frontend, which will manage the user-facing answer and feedback flow.
