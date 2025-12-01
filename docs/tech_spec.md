# Technical Specification: AI Buddy MVP

## 1. Introduction

This technical specification outlines the implementation details for the AI Buddy MVP. It is derived from the [Architecture](./architecture.md), [Epics](./epics.md), and [UX Design Specification](./ux-design-specification.md). It serves as a practical guide for developers to build the initial release, focused on the "Student" persona and document processing features.

## 2. Backend (FastAPI + Python)

The backend follows a service-oriented structure within a modular monolith.

### 2.1. Key Modules
*   **API Layer (`app/api/`)**: Routes and controllers defined using FastAPI `APIRouter`. Handles request validation (Pydantic models) and response formatting.
*   **Core Services (`app/services/`)**:
    *   `AuthService`: Handles user registration and token verification.
    *   `DocumentService`: Manages file I/O and database records for documents.
    *   `OrchestratorService`: The central logic that coordinates the "Reader" and "Coach" steps.
*   **Agents (`app/agents/`)**:
    *   `ReaderAgent`: Encapsulates OCR logic and initial text analysis (LLM prompts).
    *   `CoachAgent`: Generates specific artifacts (Flashcards, Quizzes) from the analyzed text.
*   **Workers (`app/workers/`)**:
    *   **RQ Worker**: Background process listening to Redis queues to execute long-running agent tasks (OCR, Generation) without blocking the API.

### 2.2. Key API Endpoints (MVP)

*   **Authentication**
    *   `POST /auth/register`: Create a new user.
    *   `POST /auth/token`: Login (returns JWT).
*   **Document Management**
    *   `POST /documents/upload`: Accepts `multipart/form-data` file. Saves to disk, creates DB record, enqueues "Process/OCR" job. Returns `job_id`.
    *   `DELETE /documents/{doc_id}`: Deletes file and all related data.
*   **Orchestration & Generation**
    *   `POST /documents/{doc_id}/generate/{type}`: Trigger generation for `summary`, `flashcards`, or `quiz`. Returns `job_id`.
    *   `GET /jobs/{job_id}`: Polling endpoint for frontend to check status (`queued`, `processing`, `completed`, `failed`) and retrieve result payload if done.
*   **Data Retrieval**
    *   `GET /documents`: List user's documents (History).
    *   `GET /documents/{doc_id}`: Fetch specific document metadata and available generated content.
    *   `POST /quizzes/{quiz_id}/attempt`: Submit quiz results (for progress tracking).

### 2.3. Agent Invocation Flow
1.  **Trigger**: API receives a request (e.g., "Generate Quiz").
2.  **Queue**: API adds a job to the Redis Queue (e.g., `generate_quiz_task(doc_id)`).
3.  **Execution (Worker)**:
    *   Worker dequeues task.
    *   Fetches `ConversationContext` (or document text) from DB/Redis.
    *   Invokes `CoachAgent.generate_quiz(context)`.
    *   `CoachAgent` calls LLM API.
    *   Worker saves result to DB and updates Job status to `completed`.

## 3. Frontend (Next.js + Shadcn UI)

### 3.1. Main Pages (Routes)
*   `/login`: User authentication form.
*   `/dashboard`: List of past study sessions (History/Epics 6.1).
*   `/session/new`: The "Upload Wizard" (Upload -> Process -> Study).
*   `/session/[id]`: The "Study Session View" (Summary, Flashcards, Quiz).

### 3.2. Key Components
*   **`FileUploader`**: Drag-and-drop component handling file selection and validation.
*   **`Stepper`**: Visual progress indicator for the wizard flow.
*   **`FlashcardView`**: Interactive component for the flashcard study mode (flip animation, known/unknown rating).
*   **`QuizView`**: Interactive quiz component (question display, option selection, immediate feedback).
*   **`ProgressSummary`**: Displays results after quiz completion.

### 3.3. Backend Communication
*   **Client**: Standard `fetch` or `axios` wrapper.
*   **Authentication**: All authenticated requests must include the `Authorization: Bearer <token>` header.
*   **State Management**: React Query (TanStack Query) or SWR is recommended for managing async job polling and data caching.

## 4. Data and Storage

### 4.1. Core Entities (Schema)
*   **`User`**: `id`, `email`, `password_hash`, `created_at`.
*   **`Document`**: `id`, `user_id`, `title`, `file_path` (local path), `content_text` (OCR result), `summary`, `created_at`.
*   **`FlashcardDeck`**: `id`, `document_id`, `cards` (JSONB array of front/back).
*   **`Quiz`**: `id`, `document_id`, `questions` (JSONB array of questions/options/answers).
*   **`QuizAttempt`**: `id`, `quiz_id`, `user_id`, `score`, `completed_at`.

### 4.2. Storage Strategy
*   **Files**: Stored locally in `backend/uploaded_docs/` (per Architecture ADR).
*   **Deletion (FR2.3, FR2.4)**:
    *   When `DELETE /documents/{id}` is called, the system MUST:
        1.  Remove the physical file from disk.
        2.  Delete the `Document` record from Postgres (cascading delete removes Quizzes/Flashcards).
    *   *Note: TTL (auto-deletion) will be implemented as a scheduled cron job in a future sprint, not required for MVP day 1.*

## 5. Technical Non-Functional Aspects

*   **Performance**:
    *   **Async Processing**: All file parsing and LLM generation MUST be background jobs. The API should respond in <200ms with a Job ID.
    *   **Optimistic UI**: The frontend should show "Processing" states immediately while polling occurs.
*   **Security**:
    *   **TLS**: Production endpoints must use HTTPS.
    *   **Passwords**: Hashed using `bcrypt`.
    *   **File Access**: Uploaded files are *not* served via public URL; they are only read by the backend worker.
*   **Accessibility (WCAG 2.1 AA)**:
    *   All Shadcn/UI components (based on Radix UI) ensure keyboard navigability and screen reader support.
    *   Color contrast in the "Focus" theme (Blue #0d6efd) must be verified against white backgrounds.
