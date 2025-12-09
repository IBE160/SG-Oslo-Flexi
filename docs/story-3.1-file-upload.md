# User Story 3.1: File Upload

**Epic:** [Epic 3: Document Processing & Analysis](./epics.md#epic-3-document-processing--analysis)
**Status:** Ready for Dev
**Sprint:** Sprint 3

## 1. User Story

**As a** student or self-learner,
**I want to** upload a study document (PDF, DOCX, or TXT) from my computer to the AI Buddy platform,
**So that** I can have it analyzed and processed into study materials (summaries, flashcards, and quizzes).

## 2. Context & Goal
The file upload is the entry point for the entire AI Buddy value proposition. Without a successful upload, no downstream value (summary, quiz, etc.) can be generated. The goal is to provide a frictionless, clear, and secure way for users to submit their files for processing. This story focuses solely on the **upload mechanism** and **secure storage** (handshaking with Story 3.4).

## 3. Functional Requirements

*   **FR3.1.1:** The system SHALL provide a file upload interface (drag-and-drop or file picker) on the dashboard.
*   **FR3.1.2:** The system SHALL accept files with the following extensions: `.pdf`, `.docx`, `.txt`.
*   **FR3.1.3:** The system SHALL enforce a maximum file size limit of **20MB**.
*   **FR3.1.4:** The system SHALL validate the file type (MIME type) on the backend to prevent malicious uploads (e.g., executables masked as PDFs).
*   **FR3.1.5:** Upon successful upload, the system SHALL save the file to a secure, private storage volume.
*   **FR3.1.6:** Upon successful upload, the system SHALL create a database record for the document with a status of `pending`.
*   **FR3.1.7:** The system SHALL provide immediate visual feedback to the user during the upload (progress bar or spinner) and upon completion (success message).
*   **FR3.1.8:** If the upload fails (network error, invalid type, too large), the system SHALL display a clear, user-friendly error message.

## 4. Acceptance Criteria (Gherkin)

### Scenario 1: Successful PDF Upload
**Given** I am a logged-in user on the dashboard
**And** I have a valid PDF file named `lecture_notes.pdf` (under 20MB)
**When** I drag and drop the file into the upload area
**Then** I should see a progress indicator
**And** the upload should complete successfully
**And** I should see a "Processing..." status for the document
**And** the document should appear in my document list

### Scenario 2: Invalid File Type
**Given** I am a logged-in user
**When** I attempt to upload a file named `malicious_script.exe`
**Then** the system should reject the upload immediately
**And** I should see an error message: "Invalid file type. Please upload a PDF, DOCX, or TXT file."

### Scenario 3: File Too Large
**Given** I am a logged-in user
**And** I have a PDF file larger than 20MB
**When** I attempt to upload the file
**Then** the system should reject the upload
**And** I should see an error message: "File too large. Maximum size is 20MB."

### Scenario 4: Secure Storage Validation
**Given** a file has been uploaded successfully
**When** a developer inspects the storage volume
**Then** the file should be saved with a unique identifier (UUID) as the filename
**And** the file should NOT be accessible via a direct public URL

## 5. UX & Design Notes

*   **Upload Component:** Use a clear "drop zone" with a secondary "Browse" button.
*   **Micro-copy:** Explicitly state the limits: "Supported formats: PDF, DOCX, TXT. Max size: 20MB."
*   **Feedback:** Use a determinate progress bar if possible (based on upload percentage), otherwise an indeterminate spinner.
*   **State:** After upload, the card for the document should immediately show a "Processing" badge (yellow/orange) to indicate background work is happening.

## 6. Technical Implementation Details

### Architecture Components
*   **Frontend:** `DocumentUpload` component (React/Next.js) using `shadcn/ui` and `axios` or `fetch` for `multipart/form-data`.
*   **Backend API:** `POST /api/v1/documents/` (FastAPI).
*   **Storage:** Local volume mapped to `backend/uploaded_docs/`.
*   **Database:** `documents` table (PostgreSQL).
*   **Validation:** `python-magic` for MIME type detection.

### Data Model Impact (`documents` table)
| Field | Value |
| :--- | :--- |
| `filename` | Original filename (e.g., `physics_101.pdf`) |
| `file_path` | UUID-based path (e.g., `/uploaded_docs/550e8400-e29b-41d4-a716-446655440000.pdf`) |
| `status` | `pending` |

### Security Constraints
*   **Sanitization:** Never use the user-provided filename for the actual file storage. Use `uuid.uuid4()`.
*   **Access:** Ensure the API endpoint requires a valid JWT token (`current_user`).

## 7. Non-Functional Requirements (NFRs)

*   **Performance:** The upload API should respond within 2 seconds for a 5MB file on a standard broadband connection.
*   **Reliability:** The upload process should handle network interruptions gracefully (e.g., simple retry logic on the frontend if feasible, or clear failure state).
*   **Security:** Files must never be executable on the server.

## 8. Dependencies
*   This story is a prerequisite for **Story 3.2 (OCR)** and **Story 3.3 (Reader Agent)**.
*   Depends on **Story 2.4 (Auth)** for user context.

---

## 9. Validation Notes

### 9.1. Alignment Checks
*   ✅ **Epic 3:** Matches Story 3.1 & 3.4 exactly.
*   ✅ **PRD:** FR3.1.2 matches FR2.1 in PRD (PDF, DOCX, TXT, 20MB).
*   ✅ **Tech Spec:** Architecture components (FastAPI, PostgreSQL, Local Volume) match `docs/tech-spec-epic-3.md`.

### 9.2. Completeness
*   **Testable:** Gherkin scenarios cover happy path, invalid type, and size limit.
*   **Secure:** Explicitly requires UUID filenames and backend MIME validation.

### 9.3. Corrections
*   *None required.* The story is robust and ready for implementation.