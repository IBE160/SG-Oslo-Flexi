# Brainstorm – Detailed UI/UX Component Design (2025-11-09)

- **Core Design Principles**
    - **Simplicity & Focus:** The UI must be minimal and guide the user through a single, linear task. There will be no navigation bars, sidebars, or other distracting elements for the MVP.
    - **Clarity & Communication:** The user must always understand the system's current state (e.g., waiting for upload, processing, ready for quiz) and what is expected of them.
    - **Mobile-First:** The layout will be designed for a mobile viewport first, ensuring a clean and functional experience on any device. The desktop view will be an enhanced, wider version of the mobile layout.
    - **Accessibility:** We will adhere to WCAG guidelines by ensuring sufficient color contrast, providing clear focus states for interactive elements, and using semantic HTML.

- **Component 1: The Upload View**
    - **Objective:** To provide a simple, intuitive way for the user to upload their document.
    - **Layout:** A single, centered card on a clean background.
    - **Elements:**
        - **Heading:** "Create Your AI Study Guide"
        - **Instructions:** A sub-heading clearly stating the allowed file types and size limit (e.g., "Upload a PDF, PNG, or JPG. Max 20MB.").
        - **Drop Zone:** A large, dashed-border area with a cloud-upload icon and text: "Drag & drop your file here or **click to browse**."
    - **Interaction:**
        - Clicking the zone opens the native file picker.
        - Dragging a file over the zone provides visual feedback (e.g., the border color changes).
        - An invalid file (checked client-side) shows an immediate, inline error message (e.g., "Invalid file type.") and does not initiate an upload.

- **Component 2: The Processing View**
    - **Objective:** To keep the user informed and engaged while the backend works. This view replaces the Upload View's content after a successful file submission.
    - **Layout:** The same centered card, but its content updates to show a status indicator.
    - **Elements:**
        - **Spinner/Animation:** A clean, looping animation to show that the system is active.
        - **Dynamic Status Text:** A text label below the spinner that updates in real-time to reflect the backend state. This is critical for managing user expectations.
            1.  `Uploading...`
            2.  `Analyzing document...` (OCR step)
            3.  `Generating quiz...` (LLM step)
    - **Error State:**
        - If a backend error occurs, the spinner is replaced by an error icon (e.g., a red warning triangle).
        - A clear, actionable error message is displayed (e.g., "Document quality is too low. Please try a clearer copy.").
        - A "Try Again" button is shown, which resets the view back to the initial Upload component.

- **Component 3: The Quiz View**
    - **Objective:** To present the quiz in a clean, focused, one-question-at-a-time format.
    - **Layout:** A centered card containing the question and answers.
    - **Elements:**
        - **Header:** A progress indicator, e.g., "Question 2 of 5".
        - **Question:** The question text, displayed with a large, readable font.
        - **Options:** A list of 4 buttons, each containing the text for a multiple-choice option.
    - **Interaction:**
        - The user taps/clicks one option. The selected button shows a distinct visual state (e.g., a solid background color).
        - A "Next" button at the bottom of the card becomes enabled only after an option is selected.
        - Clicking "Next" transitions to the next question. On the final question, the button text changes to "See Results".

- **Component 4: The Results View**
    - **Objective:** To provide immediate, clear feedback on the user's performance.
    - **Layout:** A final summary card.
    - **Elements:**
        - **Score Display:** A prominent, celebratory heading (e.g., "Great job! You scored **4/5**").
        - **Review List:** A scrollable list of all the questions from the quiz. Each item in the list displays:
            - The question text.
            - The user's answer, with an icon indicating if it was correct (✅) or incorrect (❌).
            - The correct answer, always highlighted for learning reinforcement.
        - **Call to Action:** Two buttons at the bottom:
            1.  **"Generate New Quiz"** (primary action, solid color).
            2.  **"Finish"** (secondary action, outline style).

- **Proposed Decision**
The MVP's UI will be a single-page application composed of four distinct, state-driven views: Upload, Processing, Quiz, and Results. The design will be minimal, mobile-first, and heavily focused on providing clear, continuous feedback to the user, especially during processing and error states. This approach will create a seamless and intuitive experience that guides the user through the core "document-to-quiz" journey.
