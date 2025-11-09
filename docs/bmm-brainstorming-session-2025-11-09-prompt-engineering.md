# Brainstorm – Prompt Engineering & LLM Strategy (2025-11-09)

- **Core Principles**
    - **Strict Grounding:** All generated content (summaries, questions, answers, distractors) must be derived *exclusively* from the text provided in the prompt's context. The prompts will explicitly forbid the use of any external knowledge.
    - **Structured Output:** All LLM outputs must be in a valid JSON format. This is a non-negotiable requirement for system reliability. We will use LLM API features like "JSON Mode" if available to enforce this.
    - **Role-Playing:** Prompts will assign a clear, expert role to the LLM (e.g., "You are an expert instructional designer...") to improve the quality and focus of the output.
    - **Efficiency and Token Management:** Prompts will be engineered to be clear and concise. We will enforce a maximum input document size to ensure the extracted text fits within the free-tier limits of our chosen LLM (e.g., Gemini API) and to manage costs.

- **Reader Agent Prompt Strategy (Pre-processing)**
    - **Objective:** To process the raw OCR text into a structured summary and a list of key terms for the Coach agent.
    - **Input:** Raw text extracted by Tesseract OCR.
    - **Prompt Skeleton:**
        ```
        System: You are a text analysis expert. Your task is to process the following document text and return a valid JSON object.

        User:
        Context:
        """
        [Insert raw OCR text here]
        """

        Instruction: From the text in the context above, perform the following two tasks:
        1. Extract the 5-10 most important key terms or phrases that represent the main topics.
        2. Write a concise, neutral summary of the document in 3-5 bullet points.

        Your entire output must be a single, valid JSON object with two keys: "key_terms" (an array of strings) and "summary_bullets" (an array of strings). Do not include any other text or explanation.
        ```

- **Coach Agent Prompt Strategy (Quiz Generation)**
    - **Objective:** To generate a high-quality, multiple-choice quiz based on the structured content from the Reader agent.
    - **Input:** The full JSON payload from the Reader agent, including the raw text sections.
    - **Prompt Skeleton:**
        ```
        System: You are an expert quiz designer. Your task is to create a multiple-choice quiz from the provided document context. You must adhere strictly to the following rules.

        User:
        Rules:
        1.  **Grounding:** All questions, correct answers, and incorrect 'distractor' answers must be based ONLY on the provided text in the 'sections' field of the JSON context.
        2.  **No External Knowledge:** Do not use any information not present in the provided text.
        3.  **Format:** Generate exactly 5 multiple-choice questions. Each question must have one correct answer and three plausible but incorrect distractors.
        4.  **JSON Output:** Your entire output must be a single, valid JSON object. The root object must have a key named "quiz_items", which is an array. Each object in the array must have these exact keys: "question" (string), "options" (an array of 4 strings), and "correctAnswerIndex" (an integer from 0 to 3).

        Context:
        ```json
        [Insert the full Reader -> Coach JSON contract here]
        ```

        Instruction: Now, generate the quiz based on the context provided, following all rules.
        ```

- **Handling Prompt Failures & Variability**
    - **Invalid JSON Output:**
        - **Problem:** The LLM returns a response that is not parsable JSON.
        - **Mitigation:**
            1.  **API Enforcement:** Use the LLM provider's "JSON Mode" if available.
            2.  **Retry Mechanism:** The orchestrator will wrap the LLM call in a `try-except` block. On a JSON parsing failure, it will automatically retry the request once. If it fails a second time, a "generation failure" error is returned to the user.
    - **Hallucinations (Ungrounded Content):**
        - **Problem:** The LLM generates content not found in the source text.
        - **Mitigation (MVP):** This is primarily a prompt-based mitigation. The rules in the prompt will be strict and repetitive about grounding. We accept a small risk of minor hallucinations for the MVP.
        - **Mitigation (Post-MVP):** Implement a "verification step" where a separate, fast LLM call checks if a generated answer is supported by the cited source text.

- **Token Management Strategy**
    - **Problem:** Very large documents could lead to excessive token usage, hitting free-tier limits or causing high costs.
    - **Strategy:**
        1.  **Input Capping:** Enforce a strict file size limit in the UI, which indirectly caps the amount of text sent to the LLM. This limit will be determined based on the chosen LLM's context window and free-tier constraints.
        2.  **Two-Step Process:** The Reader->Coach agent flow is itself a token management strategy. The Reader condenses the document into a summary, reducing the cognitive load for the Coach, which can then focus its attention on the raw text sections for question generation.

- **Proposed Decision**
Our LLM strategy will be centered on disciplined, role-based prompting that strictly enforces structured JSON output and grounding in the source text. We will use a two-agent (Reader/Coach) pipeline to first summarize and then generate the quiz. For the MVP, we will handle failures with a simple retry mechanism and manage token usage via input file size limits, accepting a minimal risk of prompt-related quality variance.
