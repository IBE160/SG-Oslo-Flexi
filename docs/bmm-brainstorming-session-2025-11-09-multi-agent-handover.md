# Brainstorm – Multi-Agent Handover (2025-11-09)

- **Must-haves (MVP)**
    - A clearly defined and versioned JSON contract for the data payload passed from the Reader agent to the Coach agent.
    - A central orchestrator service that manages the sequential execution of the agent workflow (Client → Orchestrator → Reader → Coach → Client).
    - A unique `trace_id` must be generated for every request and passed through the entire call chain for observability.
    - A simple, non-negotiable quality gate: if the Reader's OCR confidence score is below a set threshold, the handover is aborted, and an error is returned.
    - The orchestrator is responsible for validating the JSON contract before executing the handover.

- **Should-haves (next)**
    - Implement a retry mechanism with exponential backoff for transient failures in agent communication.
    - Introduce a fallback rule: if the primary Coach agent (e.g., a powerful but expensive LLM) fails, retry with a simpler, more reliable model.
    - Allow the Coach to send feedback back to the Reader (e.g., "sections were too long") for future adaptive processing.
    - Version the agents themselves, allowing the orchestrator to route requests to specific agent versions.

- **Reader → Coach JSON contract (v0)**
    - The **Reader** agent produces the following payload after processing a document.

    ```json
    {
      "contract_version": "v0",
      "trace_id": "uuid-for-this-specific-request",
      "doc_meta": {
        "filename": "lecture_notes.pdf",
        "filetype": "pdf",
        "pages": 15
      },
      "quality": {
        "ocr_confidence_score": 0.92,
        "unreadable_pages": [12]
      },
      "key_terms": ["Mitochondria", "ATP", "Cellular Respiration"],
      "summary_bullets": [
        "Mitochondria are the powerhouse of the cell.",
        "They generate most of the cell's supply of adenosine triphosphate (ATP)."
      ],
      "sections": [
        {
          "section_id": "page_1_para_1",
          "page_number": 1,
          "text": "The mitochondrion is a double-membraned organelle found in most eukaryotic organisms..."
        }
      ]
    }
    ```

    - The **Coach** agent receives the above and returns the following structure.

    ```json
    {
      "trace_id": "uuid-for-this-specific-request",
      "flashcards": [
        {
          "front": "What is the primary role of the mitochondrion?",
          "back": "To generate cellular energy (ATP).",
          "source_span": ["page_1_para_1"]
        }
      ],
      "quiz_items": [
        {
          "itemType": "MCQ",
          "question": "Which organelle is known as the 'powerhouse of the cell'?",
          "options": ["Nucleus", "Ribosome", "Mitochondrion"],
          "correctAnswerIndex": 2,
          "source_span": ["page_1_para_1"]
        }
      ]
    }
    ```

- **Orchestrator flow (single endpoint steps)**
    1.  Client POSTs a document to the `/generate-study-guide` endpoint.
    2.  **Orchestrator:** Generates `trace_id`. Invokes **Reader** agent with the document.
    3.  **Reader:** Processes the document and returns the `Reader → Coach JSON contract`.
    4.  **Orchestrator:** Validates the returned JSON. Checks `quality.ocr_confidence_score`.
    5.  **Gate:** If score < 0.85, the orchestrator immediately returns a `422 Unprocessable Entity` error to the client.
    6.  **Orchestrator:** If score is sufficient, it invokes the **Coach** agent with the full JSON payload.
    7.  **Coach:** Generates learning materials (quiz, flashcards) and returns its structured JSON output.
    8.  **Orchestrator:** Returns the Coach's payload to the client with a `200 OK` status.

- **Observability (trace IDs, timing, error logs)**
    - **Trace IDs:** The `trace_id` is the primary key for correlating logs. It must be present in every log message related to the request.
    - **Timing:** The orchestrator must log the execution duration for each agent call (e.g., `reader_call_duration_ms`, `coach_call_duration_ms`).
    - **Error Logs:** All services must emit structured (JSON) logs to stdout. A centralized logging service will collect these. Errors must include the `trace_id`, agent name, function name, and a detailed error message.

- **Risks & mitigations**
    - **Risk: Schema Drift:** The Reader or Coach agent's API changes, breaking the contract.
        - **Mitigation:** The orchestrator must perform schema validation on all incoming and outgoing payloads between agents. Implement versioning in the contract and endpoint routes (e.g., `/v0/invokeReader`).
    - **Risk: Poor Intermediate Content:** The Reader's summary or key terms are low quality, poisoning the context for the Coach.
        - **Mitigation:** The Coach should treat the `sections` text as the source of truth. The summary and key terms are supplementary context, not primary input.
    - **Risk: Debugging Complexity:** With multiple agents, it's difficult to pinpoint the source of an error.
        - **Mitigation:** Strict adherence to the observability plan is critical. Distributed tracing (via `trace_id`) is not a "nice-to-have"; it is a core requirement for debugging a multi-agent system.

- **Proposed decision**
The Reader-to-Coach handover will be explicitly managed by a central orchestrator, which enforces a versioned JSON contract and a minimum quality gate based on OCR confidence. Observability through distributed tracing (`trace_id`) and structured logging is a foundational requirement for the MVP to ensure system stability and debuggability.
