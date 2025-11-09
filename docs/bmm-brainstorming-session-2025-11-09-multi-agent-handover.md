# Brainstorming Session: Multi-Agent Handover Protocol

**Date:** 2025-11-09
**Attendees:** Gemini, BMM Team

## Objective
Define a clear and structured data handover protocol between the "Reader Agent" and the "Coach Agent" to ensure seamless collaboration and high-quality output.

---

### 1. The Core Problem

The "Reader Agent" consumes raw source material and produces structured, summarized information. The "Coach Agent" needs this structured information—not the raw text—to generate effective learning materials (quizzes, flashcards).

How do we format the data package (the "handover object") that the Reader sends to the Coach?

---

### 2. Proposed Handover Object (`HandoverV1`)

We propose a JSON object that serves as the standard data transfer object (DTO) between agents.

**`HandoverV1` JSON Schema:**

```json
{
  "metadata": {
    "sessionId": "uuid-string-12345",
    "sourceTitle": "Introduction to Quantum Physics",
    "sourceHash": "sha256-of-raw-content",
    "language": "en",
    "generatedAt": "2025-11-09T14:30:00Z"
  },
  "context": {
    "fullSummary": "A comprehensive summary of the entire document, written in clear, concise language. This serves as the main narrative context for the Coach Agent.",
    "keyConcepts": [
      {
        "term": "Quantum Superposition",
        "definition": "The principle that a quantum system can exist in multiple states at the same time until it is measured.",
        "relevance": "High"
      },
      {
        "term": "Entanglement",
        "definition": "A phenomenon where two or more quantum particles are linked in such a way that their fates are intertwined, regardless of the distance separating them.",
        "relevance": "High"
      },
      {
        "term": "Wave-Particle Duality",
        "definition": "The concept that every particle or quantum entity may be described as either a particle or a wave.",
        "relevance": "Medium"
      }
    ],
    "mainSections": [
      {
        "sectionTitle": "Chapter 1: The Basics",
        "sectionSummary": "This section introduces the fundamental ideas of quantum mechanics, contrasting it with classical physics.",
        "contentRef": "pages 1-5"
      },
      {
        "sectionTitle": "Chapter 2: Core Principles",
        "sectionSummary": "Explores superposition and entanglement in detail with examples.",
        "contentRef": "pages 6-12"
      }
    ]
  },
  "instructions_for_coach": {
    "targetAudience": "University Student (Beginner)",
    "generationGoals": ["flashcards", "multiple_choice_quiz"],
    "focusAreas": [
      "Quantum Superposition",
      "Entanglement"
    ],
    "constraints": {
      "numFlashcards": 15,
      "numQuizQuestions": 10,
      "quizDifficulty": "easy"
    }
  }
}
```

---

### 3. Breakdown of the `HandoverV1` Object

#### `metadata`
- **Purpose:** For tracking, logging, and debugging.
- **`sessionId`:** Links the entire process to a user's session.
- **`sourceHash`:** Allows caching. If the same file is uploaded again, we can skip the "Reader Agent" step if the hash matches.
- **`language`:** Ensures the "Coach Agent" generates content in the correct language (NO/EN).

#### `context`
- **Purpose:** This is the core knowledge base for the "Coach Agent". It's everything the Coach needs to know about the source material.
- **`fullSummary`:** The primary narrative. The Coach can use this to understand the overall topic and generate high-level questions.
- **`keyConcepts`:** A structured list of important terms and definitions. Perfect for generating flashcards. The `relevance` flag helps prioritize.
- **`mainSections`:** A breakdown of the document's structure. The Coach can use this to create section-specific questions or to understand the flow of the material.

#### `instructions_for_coach`
- **Purpose:** A direct command from the "Orchestrator" (the main backend service) to the "Coach Agent".
- **`targetAudience`:** Helps the Coach tailor the tone and complexity of the questions.
- **`generationGoals`:** Tells the Coach what to create (e.g., just a quiz, or flashcards and a quiz).
- **`focusAreas`:** Allows for adaptive learning. If a user struggles with certain topics, the orchestrator can instruct the Coach to generate more questions on those `keyConcepts`.
- **`constraints`:** Defines the shape of the output (e.g., how many questions to generate).

---

### 4. The Agent Workflow (Putting it all together)

1.  **User Uploads File**
    - The `Orchestrator` service receives the file.
    - It creates a `sessionId` and stores the file.

2.  **Orchestrator calls Reader Agent**
    - **Input:** Raw content (text, OCR output, or transcript).
    - **Prompt for Reader Agent:**
      > "You are a Reader Agent. Analyze the following text about [Source Title].
      > 1.  Create a concise, comprehensive summary (`fullSummary`).
      > 2.  Identify the top 5-10 `keyConcepts`. For each, provide the term, a clear definition, and a relevance score (High, Medium, Low).
      > 3.  Break the document down into its `mainSections`. Provide a title and a brief summary for each section.
      > Your output must be a JSON object containing `fullSummary`, `keyConcepts`, and `mainSections`."

3.  **Reader Agent Responds**
    - The Reader Agent processes the text and returns a JSON object with the `context` part of our `HandoverV1` object.

4.  **Orchestrator Prepares for Coach Agent**
    - The Orchestrator takes the `context` from the Reader.
    - It adds the `metadata` and `instructions_for_coach` sections to create the full `HandoverV1` object.
    - The `instructions_for_coach` are determined by the user's request (e.g., they clicked "Generate Quiz").

5.  **Orchestrator calls Coach Agent**
    - **Input:** The complete `HandoverV1` JSON object.
    - **Prompt for Coach Agent:**
      > "You are a Coach Agent. Based on the provided JSON data, your task is to generate learning materials.
      > **Context:** The user is studying '[Source Title]'. The key concepts are [list of key concepts].
      > **Your Goal:** Fulfill the instructions in the `instructions_for_coach` section.
      > **Rules:**
      > - Generate exactly `numFlashcards` flashcards from the `keyConcepts`.
      > - Generate exactly `numQuizQuestions` multiple-choice questions based on the `fullSummary` and `mainSections`.
      > - Ensure questions are suitable for a `targetAudience`.
      > - Prioritize the `focusAreas` when creating questions.
      > Your output must be a JSON object containing two keys: `flashcards` (an array of {question, answer}) and `quiz` (an array of {question, options, correctAnswerIndex})."

6.  **Coach Agent Responds**
    - The Coach Agent returns the final JSON with the learning materials.

7.  **Orchestrator Saves and Displays**
    - The Orchestrator saves the generated content to the database and sends it to the frontend.

---
### 5. Contracts & Shared State

To ensure deterministic behavior, all communication between agents (nodes) and the central state are strictly defined.

#### Message Contracts

- **`ReaderOutput`**: Produced by the Reader Agent.
  ```json
  {
    "extracted_blocks": [
      { "block_id": "p1", "text": "...", "source_page": 1 }
    ],
    "doc_meta": { "title": "...", "language": "en" }
  }
  ```
  - **Validation**: `extracted_blocks` must be a non-empty array. Each block must have a `block_id` and `text`.

- **`QuizSpec`**: Sent to the Coach Agent to request a quiz.
  ```json
  {
    "blocks_to_assess": ["p1", "p3"],
    "num_questions": 5,
    "difficulty": "MEDIUM"
  }
  ```
  - **Validation**: `blocks_to_assess` must contain valid `block_id`s. `num_questions` must be > 0.

- **`QuizResults`**: Produced by the frontend/quiz engine after a user completes a quiz.
  ```json
  {
    "quiz_id": "uuid",
    "answers": [
      { "item_id": "q1", "is_correct": true, "latency_sec": 12 },
      { "item_id": "q2", "is_correct": false, "latency_sec": 25 }
    ]
  }
  ```
  - **Validation**: `quiz_id` must be valid. `answers` array must match the number of questions.

- **`CoachNotes`**: Asynchronous feedback from the Coach Agent about user performance.
  ```json
  {
    "notes": [
      "User struggles with 'Quantum Entanglement'.",
      "User consistently answers `HARD` questions incorrectly."
    ]
  }
  ```

#### Single Source of Truth: `SessionState`

A single, unified state object is maintained by the orchestrator for the lifecycle of a study session.

```json
{
  "session_id": "uuid-123",
  "user_id": "user-abc",
  "doc_meta": {
    "filename": "lecture.pdf",
    "uploaded_at": "timestamp"
  },
  "extracted_blocks": [
    { "block_id": "p1", "text": "...", "source_page": 1 }
  ],
  "quiz_items": [
    { "item_id": "q1", "question": "...", "difficulty": "MEDIUM" }
  ],
  "results": [
    { "item_id": "q1", "is_correct": true, "timestamp": "..." }
  ],
  "notes": [
    "User struggles with 'Quantum Entanglement'."
  ]
}
```

---
### 6. Error Taxonomy & Retries

- **`400 Bad Request`**: Invalid message contract. The request body fails Pydantic/JSON schema validation. No retry.
- **`422 Unprocessable Entity`**: The input is valid, but fails a quality gate (e.g., OCR confidence too low, text too short). No retry; requires user action.
- **`502 Bad Gateway`**: An upstream AI service (e.g., Gemini) fails.
  - **Retry Policy**: Implement exponential backoff.
    - 1st retry: after 1 second.
    - 2nd retry: after 3 seconds.
    - 3rd retry: after 5 seconds.
  - If all retries fail, return a `502` to the client with a `trace_id` for debugging.
- **`504 Gateway Timeout`**: An upstream AI service takes too long to respond. Same retry policy as `502`.

---
### 7. Observability

To ensure transparency and debuggability of the multi-agent workflow, detailed logs will be captured at each stage.

- **Per-Node Logging**: Each agent (Reader, Coach) and the Orchestrator will log:
  - `input_hash`: SHA256 hash of the input payload.
  - `output_hash`: SHA256 hash of the output payload.
  - `duration_ms`: Time taken for the agent to process the request.
  - `tokens_used`: Number of tokens consumed by the LLM (if applicable).
  - `errors`: Any errors encountered during processing.
- **Trace ID**: The `session_id` will serve as the `trace_id`, propagated across all logs for a given session.
- **Structured Logs**: All logs will be in JSONL format, making them easy to parse and aggregate by a central logging system.

---
### 8. E2E Scenarios

These scenarios define the critical end-to-end paths that must be tested to ensure the multi-agent system functions as expected.

- **Happy Path (Text-based PDF)**:
  - **Scenario**: User uploads a clean, text-based PDF.
  - **Expected Flow**: PDF -> Reader Agent (pdfminer) -> Orchestrator -> Coach Agent -> Quiz/Flashcards.
  - **Acceptance Criteria**:
    - Quiz and flashcards are generated successfully.
    - Content is accurate and relevant to the input PDF.
    - Response time is within acceptable limits (e.g., < 30 seconds).

- **Fallback Path (Scanned PDF with OCR)**:
  - **Scenario**: User uploads a clean, scanned PDF.
  - **Expected Flow**: PDF -> OCR Pipeline (OCRmyPDF) -> Reader Agent -> Orchestrator -> Coach Agent -> Quiz/Flashcards.
  - **Acceptance Criteria**:
    - Quiz and flashcards are generated successfully.
    - Content is accurate and relevant to the input PDF (allowing for minor OCR imperfections).
    - OCR confidence score is logged and above the threshold.

- **Low-Confidence Triggers Manual Review**:
  - **Scenario**: User uploads a low-quality scanned PDF.
  - **Expected Flow**: PDF -> OCR Pipeline (OCRmyPDF) -> Orchestrator flags for manual review.
  - **Acceptance Criteria**:
    - The system returns a `422 Unprocessable Entity` with a clear message.
    - The session state indicates a pending manual review.
    - No quiz or flashcards are generated.

---
### 9. Build Checklist (MVP)

- [ ] Implement the Orchestrator service to manage agent calls.
- [ ] Define and implement Pydantic models for all message contracts (`ReaderOutput`, `QuizSpec`, `QuizResults`, `CoachNotes`).
- [ ] Implement the `SessionState` object and its persistence.
- [ ] Integrate the Reader Agent with the OCR pipeline.
- [ ] Integrate the Coach Agent with the Quiz Engine.
- [ ] Implement the error taxonomy and retry logic for upstream AI calls.
- [ ] Set up structured logging with `session_id` as `trace_id`.
- [ ] Develop E2E tests for the happy path, fallback path, and low-confidence scenarios.

---
### Advantages of this Protocol
- **Decoupled:** The Reader and Coach agents don't need to know about each other. They only communicate through the Orchestrator via the `HandoverV1` object.
- **Structured & Predictable:** Using a clear JSON schema makes the process reliable and easy to debug.
- **Extensible:** We can add new fields to the `HandoverV1` object later. For example, we could add a `diagrams` array if the Reader Agent can identify and describe images.
- **Testable:** We can easily write unit tests for each agent by feeding them mock `HandoverV1` objects.