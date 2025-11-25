# AI Buddy - Epics

> **Note on IBE160 MVP Scope:** The epics below describe the full vision for AI Buddy. For the IBE160 course project, the MVP is strictly focused on:
> *   A single **“Student” persona** (no teacher dashboards or multi-tenant management).
> *   **Document upload with OCR only** (no audio-to-text functionality).
> *   **Document-first prompting** on extracted text (no vector database or full RAG pipeline).

## Epic 1: Foundation & Core Setup

**Goal:** Establish the foundational infrastructure for the AI Buddy project, including project setup, core dependencies, and a basic CI/CD pipeline. This epic will not deliver user-facing features but is essential for all future development.

### Stories:

**Story 1.1: Project Initialization**

*   **As a developer,** I want to initialize the project structure with a frontend (Next.js) and backend (FastAPI) application, so that we have a clean and organized codebase to start with.
*   **Acceptance Criteria:**
    *   Given the project repository is cloned,
    *   When I run the setup script,
    *   Then a `frontend` directory with a new Next.js application is created.
    *   And a `backend` directory with a new FastAPI application is created.

**Story 1.2: Dependency Management**

*   **As a developer,** I want to set up dependency management for both the frontend and backend, so that we can easily add and manage project dependencies.
*   **Acceptance Criteria:**
    *   Given the project is initialized,
    *   When I navigate to the `frontend` directory,
    *   Then I can install dependencies using `npm install`.
    *   And when I navigate to the `backend` directory,
    *   Then I can install dependencies using `pip install -r requirements.txt`.

**Story 1.3: Basic CI/CD Pipeline**

*   **As a developer,** I want to set up a basic CI/CD pipeline that runs on every push to the main branch, so that we can ensure the code is always in a deployable state.
*   **Acceptance Criteria:**
    *   Given a GitHub repository is set up,
    *   When I push a commit to the `main` branch,
    *   Then a GitHub Actions workflow is triggered.
    *   And the workflow runs linting and unit tests for both the frontend and backend.

## Epic 2: User Authentication & Onboarding

**Goal:** Implement a secure user authentication system and a smooth onboarding experience to guide new users to their "Aha!" moment.

### Stories:

**Story 2.1: User Registration**

*   **As a new user,** I want to be able to register for an account using my email and a password, so that I can access the application.
*   **Acceptance Criteria:**
    *   Given I am on the registration page,
    *   When I enter my email and a valid password,
    *   Then my account is created and I am logged in.

**Story 2.2: User Login**

*   **As a registered user,** I want to be able to log in to my account, so that I can access my saved progress and materials.
*   **Acceptance Criteria:**
    *   Given I am on the login page,
    *   When I enter my correct email and password,
    *   Then I am logged in and redirected to my dashboard.

**Story 2.3: Basic Onboarding**

*   **As a new user,** I want to be guided through the core features of the application, so that I can quickly understand how to use it.
*   **Acceptance Criteria:**
    *   Given I have just registered,
    *   When I log in for the first time,
    *   Then I am shown a brief, interactive tutorial that guides me through uploading a document and generating a quiz.

## Epic 3: Document Processing & Analysis

**Goal:** Build the core document processing pipeline, including file upload, OCR, and the "Reader" agent for content analysis.

### Stories:

**Story 3.1: File Upload**

*   **As a user,** I want to be able to upload a document (PDF, DOCX, TXT) from my computer, so that I can have it analyzed.
*   **Acceptance Criteria:**
    *   Given I am on the dashboard,
    *   When I select a valid file to upload,
    *   Then the file is uploaded to the server and a "processing" state is displayed.

**Story 3.2: OCR for Scanned Documents**

*   **As a user,** I want the system to be able to read text from scanned documents, so that I can use my handwritten notes.
*   **Acceptance Criteria:**
    *   Given I have uploaded a scanned PDF,
    *   When the document is processed,
    *   Then the text is extracted using OCR and made available for analysis.

**Story 3.3: "Reader" Agent Analysis**

*   **As a user,** I want the "Reader" agent to analyze the content of my uploaded document, so that it can be used to generate study materials.
*   **Acceptance Criteria:**
    *   Given a document has been uploaded and processed,
    *   When the analysis is complete,
    *   Then a summary and key concepts are extracted and stored.

## Epic 4: AI-Powered Content Generation

**Goal:** Implement the "Coach" agent to generate summaries, flashcards, and quizzes from the analyzed document content.

### Stories:

**Story 4.1: Summary Generation**

*   **As a user,** I want to receive a concise summary of my uploaded document, so that I can quickly understand the main points.
*   **Acceptance Criteria:**
    *   Given a document has been analyzed,
    *   When I request a summary,
    *   Then a summary of the document is displayed.

**Story 4.2: Flashcard Generation**

*   **As a user,** I want to generate flashcards from my document, so that I can practice active recall.
*   **Acceptance Criteria:**
    *   Given a document has been analyzed,
    *   When I request flashcards,
    *   Then a set of question-and-answer flashcards is generated and displayed.

**Story 4.3: Quiz Generation**

*   **As a user,** I want to generate a quiz from my document, so that I can test my knowledge.
*   **Acceptance Criteria:**
    *   Given a document has been analyzed,
    *   When I request a quiz,
    *   Then a 5-question multiple-choice quiz is generated and displayed.

## Epic 5: Learning & Assessment

**Goal:** Create the user-facing learning experience, including the quiz interface, flashcard review, and results display.

### Stories:

**Story 5.1: Flashcard Review**

*   **As a user,** I want to be able to review my generated flashcards, so that I can study the material.
*   **Acceptance Criteria:**
    *   Given I have generated flashcards,
    *   When I start a review session,
    *   Then I am shown one flashcard at a time, with the ability to flip it and mark it as "known" or "unknown".

**Story 5.2: Quiz Interface**

*   **As a user,** I want to be able to take the generated quiz, so that I can assess my understanding.
*   **Acceptance Criteria:**
    *   Given I have generated a quiz,
    *   When I start the quiz,
    *   Then I am presented with one question at a time, with multiple-choice options.

**Story 5.3: Quiz Results**

*   **As a user,** I want to see my quiz results after completing a quiz, so that I can understand my performance.
*   **Acceptance Criteria:**
    *   Given I have completed a quiz,
    *   When I submit my answers,
    *   Then I am shown my score and a breakdown of which questions I answered correctly and incorrectly.

## Epic 6: Basic Progress Tracking

**Goal:** Implement the basic progress tracking features, allowing users to see their quiz history and scores.

### Stories:

**Story 6.1: Quiz History**

*   **As a user,** I want to be able to see a history of the quizzes I have taken, so that I can track my progress over time.
*   **Acceptance Criteria:**
    *   Given I have taken at least one quiz,
    *   When I navigate to my dashboard,
    *   Then I can see a list of my past quizzes, with the date and score for each.

**Story 6.2: Basic Progress Dashboard**

*   **As a user,** I want to have a simple dashboard that shows my overall progress, so that I can stay motivated.
*   **Acceptance Criteria:**
    *   Given I have taken at least one quiz,
    *   When I view my dashboard,
    *   Then I can see a summary of my average quiz score and the number of quizzes I have completed.
