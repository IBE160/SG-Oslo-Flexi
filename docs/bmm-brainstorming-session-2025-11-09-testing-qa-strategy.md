# Brainstorm – Testing & QA Strategy (2025-11-09)

- **Core QA Principles**
    - **Automation First:** Every test that can be automated, will be. This is crucial for maintaining velocity and confidence.
    - **Layered Testing Pyramid:** We will implement a standard testing pyramid: a broad base of fast unit tests, a smaller layer of integration tests, and a sharp peak of end-to-end (E2E) tests.
    - **AI Quality as a Feature:** We recognize that the quality of the AI-generated content is a core feature. A significant part of our strategy must be dedicated to validating the relevance, accuracy, and structure of the LLM's output.
    - **CI/CD Integration:** All automated tests will be executed in our GitHub Actions pipeline on every commit to the main branches, gating any deployments.

- **Layer 1: Unit Testing**
    - **Objective:** To test individual functions and UI components in complete isolation.
    - **Frontend (React):**
        - **Tools:** **Vitest** (test runner) and **React Testing Library**.
        - **Targets:** Individual React components (e.g., "Does the upload button show the correct text?"), UI state logic, and utility functions. All backend calls will be mocked.
    - **Backend (Python/FastAPI):**
        - **Tools:** **Pytest**.
        - **Targets:** Business logic within the orchestrator (e.g., the OCR quality gate), Pydantic data models, and helper functions. All external services (GCS, Pub/Sub, OCR, LLM) will be mocked.

- **Layer 2: Integration Testing**
    - **Objective:** To test the interaction between different services and components.
    - **Backend Service Integration:**
        - **Tools:** **Pytest** with FastAPI's `TestClient`.
        - **Targets:** We will test the full orchestrator API flow, ensuring the endpoints correctly call our internal services and handle responses. We will use emulators (e.g., for Google Cloud Storage) in the CI environment to test cloud integrations without using live services.
    - **AI Prompt Integration (Critical Test):**
        - **Objective:** To validate that our prompts produce the desired output from the actual LLM API.
        - **Strategy:** We will create a small test suite that runs on a schedule or before a release.
            1.  It will use a "golden set" of 2-3 sample documents.
            2.  It will call the real Reader and Coach agent functions, making live API calls to the Gemini API.
            3.  **Assertions:** The test will assert that the LLM response:
                - Is valid, parsable JSON.
                - Adheres to the specified schema (e.g., contains a `quiz_items` array of length 5).
                - Does not contain obvious errors or placeholder text.

- **Layer 3: End-to-End (E2E) Testing**
    - **Objective:** To simulate a full user journey from the browser to the backend and back.
    - **Tool:** **Playwright**.
    - **Test Scenarios:**
        1.  **The Happy Path:** A script will launch a browser, upload a known-good sample document, wait for processing, navigate through the entire quiz, and assert that the results page shows the expected score.
        2.  **Invalid Input Path:** A script will attempt to upload a file that is too large or of the wrong type and assert that the correct UI error message is displayed.
        3.  **Processing Failure Path:** A script will use a test-only endpoint to force a backend error (e.g., "low OCR quality") and assert that the frontend correctly displays the corresponding error state.

- **Special Focus: AI Quality Assurance**
    - **Objective:** To specifically address the non-deterministic and qualitative nature of LLM output.
    - **MVP Strategy:**
        - **Snapshot Testing:** For our AI Prompt Integration tests, we will store the "golden" JSON output as a snapshot. Future test runs will compare their output against this snapshot to detect any major, unexpected changes or regressions in the LLM's behavior.
        - **Manual Review:** Before the first release, the development team will conduct a manual review campaign, testing the system with at least 20 diverse documents (different lengths, topics, formats) to qualitatively assess the real-world quality of the generated quizzes.
    - **Post-MVP Strategy:**
        - **LLM-as-Evaluator:** We will explore creating an "evaluator" agent. This agent would receive a question, its answer, and the source text, and a second LLM call would be used to judge if the answer is factually supported by the text.
        - **Human Feedback Loop:** We will consider adding a simple "Was this question helpful?" (👍/👎) feedback mechanism in the UI to collect data for future prompt improvements.

- **Proposed Decision**
Our QA strategy will be heavily automated and integrated into our CI/CD pipeline, using a layered approach with Vitest, Pytest, and Playwright. The unique challenge of AI quality will be addressed in the MVP through a combination of "golden set" prompt integration tests that validate the structure of LLM outputs and a rigorous manual review process to ensure the qualitative accuracy of the generated content before launch.
