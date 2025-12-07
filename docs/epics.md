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

**Story 1.4: Database Setup (PostgreSQL)**

*   **As a developer,** I want to set up PostgreSQL as the primary database, so that the application has a robust and persistent storage layer.
*   **Acceptance Criteria:**
    *   Given a local or cloud PostgreSQL instance is available,
    *   When I configure the backend application,
    *   Then I can successfully connect to the database.
    *   And I can run basic migrations to create initial tables (e.g., users table).

**Story 1.5: Background Job Queue Setup (Redis/RQ)**

*   **As a developer,** I want to set up Redis and RQ (Redis Queue), so that time-consuming tasks like OCR and AI generation can be processed in the background without blocking the user interface.
*   **Acceptance Criteria:**
    *   Given a Redis instance is running,
    *   When I configure the backend to use RQ,
    *   Then I can enqueue a test job from an API endpoint.
    *   And a separate worker process successfully executes the job and logs the result.

**Story 1.6: Stateful Orchestrator Skeleton**

*   **As a developer,** I want to implement a basic 'Stateful Orchestrator' skeleton in the backend, so that we can manage the multi-step process of document analysis and content generation.
*   **Acceptance Criteria:**
    *   Given the backend application is running,
    *   When a document upload event occurs,
    *   Then the orchestrator creates a workflow instance with a tracked state (e.g., 'uploaded', 'processing', 'completed').
    *   And the orchestrator can transition between these states based on job completion events.

## Epic 2: User Authentication & Onboarding

**Goal:** Implement a secure user authentication system and a smooth onboarding experience to guide new users to their "Aha!" moment.

### Stories:

**Story 2.1: User Registration** (Status: Done)

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

**Story 2.4: Authentication Integration (NextAuth.js)**

*   **As a developer,** I want to integrate NextAuth.js into the frontend application, so that we have a secure and standard way to handle user sessions and protection.
*   **Acceptance Criteria:**
    *   Given the frontend application is running,
    *   When a user logs in,
    *   Then a secure session (JWT-based) is created and stored.
    *   And protected routes redirect unauthenticated users to the login page.

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

**Story 3.4: Secure Temporary Storage**

*   **As a system,** I want to securely store uploaded documents temporarily, so that they are available for processing but not exposed or retained indefinitely.
*   **Acceptance Criteria:**
    *   Given a user uploads a file,
    *   When the file is saved to the storage volume,
    *   Then it is not accessible via a public URL.
    *   And it is stored with a unique identifier associated with the user session or ID.

**Story 3.5: Document & Content Deletion**

*   **As a user (or system administrator),** I want uploaded documents and generated content to be deleted upon request or after a set time, so that my data privacy is respected.
*   **Acceptance Criteria:**
    *   Given a document has been processed and stored,
    *   When the user clicks "Delete" OR a defined TTL (Time-To-Live) expires,
    *   Then the original file and all associated database records (summary, quiz) are permanently removed from the system.

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

## Epic 7: Quality Assurance & UX Excellence

**Goal:** Ensure the application is robust, user-friendly, and accessible to all users.

### Stories:

**Story 7.1: Accessibility Compliance (WCAG 2.1 AA)**

*   **As a user with disabilities,** I want the application to be accessible and navigable using assistive technologies, so that I can use the tool effectively.
*   **Acceptance Criteria:**
    *   Given the application is deployed,
    *   When verified against WCAG 2.1 Level AA guidelines (e.g., using tools like axe-core or Lighthouse),
    *   Then there are no critical or serious accessibility violations (proper contrast, keyboard navigation, focus states, and screen reader support).
