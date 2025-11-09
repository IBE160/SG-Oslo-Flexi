# Brainstorm – Edge Cases & Failure Modes (2025-11-09)

- **Input/ingestion (size/type caps, multi-image OCR handling)**
    - **File Size/Type Limits:**
        - **Edge Case:** A user uploads a 1GB video file or a 200-page, high-resolution PDF.
        - **Failure Mode:** The request times out, the server runs out of memory, or incurs unexpectedly high processing costs.
        - **MVP Handling:** Enforce strict limits at the ingress level. Whitelist allowed MIME types (`pdf`, `png`, `jpeg`) and reject others with a `415 Unsupported Media Type` error. Enforce a max file size (e.g., 20MB) and reject larger files with a `413 Payload Too Large` error. These limits must be clearly communicated in the UI.
    - **Multi-Image Documents:**
        - **Edge Case:** A user uploads five separate JPG files that represent pages 1-5 of a single document.
        - **Failure Mode:** The system treats each image as a separate, unrelated document, losing the overall context required for a coherent study guide.
        - **MVP Handling:** This is out of scope for the MVP. The UI will only support single-file uploads per session. Each upload is treated as a standalone document.
        - **Post-MVP Strategy:** The UI should be updated to allow users to upload multiple images in one batch, reorder them, and submit them as a single, composite document.

- **Processing (low OCR confidence review step, generation retry/fallback)**
    - **Low OCR Confidence:**
        - **Edge Case:** A submitted document is blurry, skewed, or contains heavy artifacts, resulting in an OCR confidence score below the quality gate threshold.
        - **Failure Mode:** The user is blocked without a clear reason.
        - **MVP Handling:** The orchestrator aborts the handover and returns a specific error message: "Processing failed. The document quality is too low for our system to read accurately. Please try again with a clearer copy."
        - **Post-MVP Strategy:** For scores in a "gray area" (e.g., 0.70-0.85), redirect the user to a "Review & Correct" interface where they can manually edit the extracted text before it's sent to the Coach agent.
    - **Generation Failure:**
        - **Edge Case:** The Coach agent's LLM API call fails due to a timeout, rate limit, or temporary outage.
        - **Failure Mode:** The user sees a generic, unhelpful "Internal Server Error".
        - **MVP Handling:** The orchestrator will catch the exception, log the `trace_id` and error details, and return a user-friendly error: "We were unable to generate the study guide at this moment. Please try again in a few minutes."
        - **Post-MVP Strategy:** Implement a retry-with-fallback policy. The orchestrator retries the primary LLM once; if it fails again, it makes a final attempt with a smaller, faster, and more reliable secondary LLM.

- **Output quality (source_span, topic tags, duplicate checks)**
    - **Incorrect Source Span:**
        - **Edge Case:** The LLM correctly answers a question but hallucinates the `source_span`, linking it to an irrelevant part of the document.
        - **Failure Mode:** The user loses trust in the system when they try to verify an answer.
        - **MVP Handling:** This is primarily a prompt engineering challenge. The prompt must be explicit that a correct `source_span` is a mandatory part of a valid response.
        - **Post-MVP Strategy:** Implement a post-processing validation step. Calculate the semantic similarity between the generated content (e.g., a quiz answer) and the text at its cited `source_span`. If the similarity is below a threshold, flag the item for internal review or discard it.
    - **Duplicate Content:**
        - **Edge Case:** The LLM generates two quiz questions that are worded differently but test the exact same fact.
        - **Failure Mode:** The user receives a low-quality, repetitive quiz.
        - **MVP Handling:** This is an acceptable risk for the MVP. The prompt will include an instruction to ensure question diversity.
        - **Post-MVP Strategy:** Before returning the quiz to the user, calculate text embeddings for each question. Compare all pairs and if the cosine similarity between any two is above a high threshold (e.g., >0.95), discard one and regenerate.

- **Language handling (NO/EN detection/toggle)**
    - **Edge Case:** A user uploads a document written in Norwegian (NO).
    - **Failure Mode:** The system, expecting English (EN), produces a nonsensical or mixed-language output.
    - **MVP Handling:** The system will be designed and prompted for English-only. This limitation will be explicitly stated in the UI (e.g., "Please upload English documents only").
    - **Post-MVP Strategy:** The Reader agent will incorporate a language detection step and include the result (e.g., `lang: "no"`) in the `doc_meta`. The orchestrator will use this to inject language-specific instructions into the Coach agent's prompt, ensuring the output matches the source language.

- **Privacy & lifecycle (per-session delete, export constraints)**
    - **Data Retention:**
        - **Edge Case:** A user uploads a document containing sensitive personal or business information.
        - **Failure Mode:** The data is stored indefinitely on the server, creating a significant privacy and security liability.
        - **MVP Handling:** Implement a strict, non-negotiable data lifecycle policy. All uploaded documents and their derivatives are deleted from storage immediately after the user session ends or after a short, fixed TTL (e.g., 1 hour), whichever comes first. This policy must be transparently communicated to the user.
    - **Copyright and Export:**
        - **Edge Case:** A user uploads a copyrighted textbook and wants to export the generated quiz to share with others.
        - **Failure Mode:** The service could be seen as facilitating copyright infringement.
        - **MVP Handling:** No "export" or "share" functionality will be built for the MVP. All generated content is ephemeral and only accessible within the user's active session. The terms of service will state that users are responsible for ensuring they have the rights to any content they upload.

- **Proposed decision**
For the MVP, we will prioritize safety and a clear user experience by implementing strict input validation and a session-based data deletion policy. Failures will be handled by returning explicit, user-friendly error messages, deferring more complex recovery mechanisms like review steps and fallback models to a post-MVP phase.
