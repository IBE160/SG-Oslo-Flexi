# Brainstorm – User Flows (2025-11-09)

- **Primary User Persona & Goal**
    - **Persona:** The Learner. This could be a student with lecture notes, a professional reviewing a manual, or anyone needing to internalize information from a document.
    - **Context:** The user is time-constrained and wants an efficient way to self-assess their understanding of a specific document.
    - **Primary Goal:** To transform a static document into an interactive quiz with minimal effort.

- **Core User Flow: The "Happy Path"**
    - This flow describes the ideal user journey where everything works as expected.
    1.  **Start & Upload:**
        - The user lands on a simple, single-purpose page with a clear call to action: "Upload Your Document to Start".
        - The user drags and drops (or selects) a valid file (e.g., a 5-page PDF under 20MB).
    2.  **Processing Feedback:**
        - The UI immediately updates to show a non-blocking progress indicator.
        - It communicates the system's status clearly: "Reading your document...", "Preparing your quiz...".
    3.  **Quiz Interaction:**
        - Once processing is complete, the view transitions to the quiz interface.
        - Question 1 of 5 is displayed with its multiple-choice options.
        - The user selects an answer and clicks "Next". The flow repeats until the last question is answered.
    4.  **Review & Completion:**
        - The final screen displays the user's score (e.g., "You scored 4/5!").
        - A simple review list shows each question, the user's answer, and the correct answer for immediate learning.
    5.  **End of Flow:**
        - The user is presented with two clear options: "Generate a New Quiz" (re-runs the Coach agent on the same document) or "Finish".
        - Clicking "Finish" clears the session. All associated data is purged from the server as per the data retention policy.

- **Alternative Flow 1: Invalid Input**
    - **Trigger:** The user attempts to upload a file that the system cannot process.
    - **User Action:** User selects an invalid file (e.g., `project.zip` or a 50MB PDF).
    - **System Response:** The UI provides **immediate, client-side validation** before the upload begins.
    - **User Feedback:** A clear, contextual error message appears (e.g., "Invalid file type. Please use PDF, PNG, or JPG." or "File exceeds the 20MB limit."). The upload button may be temporarily disabled. The flow stops until the user provides a valid file.

- **Alternative Flow 2: Processing Failure**
    - **Trigger:** The backend encounters an issue after a valid file has been uploaded.
    - **Path A: Low-Quality Document (Reader Agent Failure)**
        - **User Action:** User uploads a blurry photo of a textbook page.
        - **System Response:** The backend's OCR quality gate returns a low confidence score. The orchestrator aborts the process.
        - **User Feedback:** The UI's progress indicator changes to an error state: "Couldn't read the document. Please try again with a clearer, higher-quality copy."
    - **Path B: AI Generation Error (Coach Agent Failure)**
        - **User Action:** User uploads a valid document, and OCR is successful.
        - **System Response:** The Coach agent (LLM) fails to generate a quiz (e.g., API outage, malformed response). The orchestrator catches the error.
        - **User Feedback:** The UI displays a specific error: "Sorry, we couldn't generate a quiz for this document. Please try again in a moment."

- **UI/UX Considerations**
    - **Clarity over clutter:** The interface must remain focused on the single task at hand. Avoid any unnecessary navigation or features for the MVP.
    - **Communicate system status:** The user must never be left wondering what is happening. Use clear, human-readable text for loading and error states.
    - **Actionable errors:** Error messages should, where possible, tell the user how to fix the problem.
    - **Ephemeral experience:** The user should understand that their session is temporary and no account is needed. This builds trust by simplifying the privacy proposition.

- **Proposed Decision**
The MVP will focus on a single, seamless "happy path" from upload to quiz completion. Crucially, the alternative flows for invalid input and processing failures must be implemented with robust, user-friendly error messaging to ensure the user experience does not feel broken or confusing when edge cases occur.
