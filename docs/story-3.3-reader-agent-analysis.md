# Story 3.3: "Reader" Agent Analysis

Status: drafted

## Story

As a user,
I want the "Reader" agent to analyze the content of my uploaded document,
so that it can be used to generate study materials.

## Functional Requirements

- **FR6.1:** The backend SHALL orchestrate a "Reader" agent to process and analyze uploaded documents.
- **FR3.1:** The system SHALL generate a concise summary from the uploaded document.
- **FR3.4:** All generated content (summaries, flashcards, quizzes) SHALL be grounded in the original uploaded document.

## Non-Functional Requirements

- **NFR8.1.1:** Summaries SHALL be generated within 10 seconds for documents up to 20MB.

## Constraints

- The "Reader" agent's analysis is the foundational step for all subsequent AI-powered content generation (summaries, flashcards, quizzes).
- The analysis must be grounded in the provided document text to avoid hallucinations.

## Data Flow

1.  **Input:** The `Stateful Orchestrator` receives a request containing the `session_id`.
2.  The `Orchestrator` retrieves the `ConversationContext` from Redis, which includes the `raw_text` of the uploaded document.
3.  The `Orchestrator` routes the request to the `ReaderAgent`, passing the `ConversationContext`.
4.  **Processing:** The `ReaderAgent` analyzes the `raw_text` to extract key concepts and generate a summary.
5.  **Output:** The `ReaderAgent` returns an updated `ConversationContext` object containing the generated `summary` and extracted `key_concepts`.
6.  The `Orchestrator` persists the updated context to Redis.

## UX Notes

- The user interface should display a "processing" or "analyzing" state to the user while the "Reader" agent is working.
- Upon completion, the UI should be updated to indicate that the analysis is complete and the user can proceed to generate study materials.

## Dependencies

- **Story 3.1: File Upload:** A document must be successfully uploaded and its text extracted.
- **Story 3.2: OCR for Scanned Documents:** For scanned documents, the OCR process must have completed successfully to provide the `raw_text`.
- **Stateful Orchestrator:** The orchestrator must be able to correctly route requests to the "Reader" agent.

## Acceptance Criteria

1.  **Given** a document has been successfully uploaded and its text extracted (via OCR if necessary),
2.  **When** the `Stateful Orchestrator` routes the analysis request to the "Reader" agent,
3.  **Then** the "Reader" agent SHALL process the document's `raw_text`.
4.  **And** the agent SHALL generate a concise summary of the document.
5.  **And** the agent SHALL extract a list of key concepts from the document.
6.  **And** the generated summary and key concepts SHALL be stored in the user's session context.
7.  **And** the entire analysis process SHALL be completed within the time defined by **NFR8.1.1**.

## Tasks / Subtasks

- [ ] **Backend:**
    - [ ] Implement the `ReaderAgent` service. (AC: #3, #4, #5, #6)
        - [ ] Add a method to receive the `ConversationContext`.
        - [ ] Implement the logic to call the LLM with a prompt for summarization and key concept extraction.
        - [ ] Implement the logic to parse the LLM response and update the `ConversationContext`.
    - [ ] **Stateful Orchestrator:**
        - [ ] Add a routing rule to direct analysis requests to the `ReaderAgent`. (AC: #2)
- [x] **Testing:**
    - [x] Write unit tests for the `ReaderAgent` service to verify LLM interaction and context updates. (AC: #4, #5, #6)
    - [x] Write an integration test to ensure the `Stateful Orchestrator` correctly routes a request to the `ReaderAgent` and the session context is updated. (AC: #1, #2, #6)
    - [x] Write a performance test to ensure the analysis completes within the NFR timeframe. (AC: #7)

## Dev Notes

- The prompt for the "Reader" agent should be carefully engineered to produce a high-quality summary and a structured list of key concepts.
- The `ConversationContext` update should be handled atomically to prevent race conditions.
- Logging should be implemented to trace the flow of data through the orchestrator and the agent for debugging purposes.

### Project Structure Notes

- The new `ReaderAgent` should be implemented in `backend/app/services/reader_agent.py`.
- The routing logic in the `Stateful Orchestrator` should be updated in `backend/app/services/orchestrator.py`.
- Tests should be added in `backend/tests/services/`.

### References

- [Source: docs/epics.md#epic-3-document-processing-analysis]
- [Source: docs/PRD.md#7-functional-requirements]
- [Source: docs/architecture.md#stateful-orchestrator]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

---
## Readiness Notes

**Quality Gate Status:** 🛑 **FAIL** (2025-12-10)

**Reason for Failure:**
- **P0 Coverage:** 0% (Threshold: 100%). None of the 7 critical acceptance criteria have corresponding tests.

**Blocker:**
- Development is **BLOCKED**. No implementation code should be merged until the planned test suite is in place and this gate is re-evaluated.

**Next Steps:**
1.  **Implement Tests:** The developer assigned to this story must first implement the unit, integration, and performance tests as defined in the "Tasks / Subtasks" section.
2.  **Re-run Traceability:** Once the tests are implemented and passing, the `*trace` workflow must be run again to verify that 100% P0 coverage has been achieved.
3.  **Re-evaluate Gate:** The quality gate will be re-evaluated based on the new traceability report.

**References:**
- [Traceability Matrix: docs/traceability-matrix-story-3.3.md](docs/traceability-matrix-story-3.3.md)
- [Quality Gate Decision: docs/gate-decision-story-3.3.md](docs/gate-decision-story-3.3.md)
