# User Story 3.2: OCR for Scanned Documents

**Epic:** [Epic 3: Document Processing & Analysis](./epics.md#epic-3-document-processing--analysis)
**Status:** Done
**Sprint:** Sprint 3

## 1. User Story

**As a** user,
**I want** the system to automatically extract text from my uploaded documents, including scanned PDFs and images,
**So that** I can use my handwritten notes and non-digital study materials for generating summaries and quizzes.

## 2. Context & Goal

Following the successful upload of a document (Story 3.1), the system must now process the file to extract its textual content. This is a critical step for the "Reader" agent (Story 3.3), which relies on raw text to perform analysis.

The challenge is to handle various formats:
1.  **Native PDFs/DOCX/TXT:** Text can be extracted directly (fast, cheap).
2.  **Scanned PDFs/Images:** Text is embedded in pixels and requires Optical Character Recognition (OCR) via Google Cloud Vision (slower, cost implication).

This story implements the **asynchronous processing pipeline** that detects the document type and applies the appropriate extraction strategy without blocking the user interface.

## 3. Functional Requirements

*   **FR3.2.1:** The system SHALL process documents asynchronously using a background worker (Redis/RQ).
*   **FR3.2.2:** The system SHALL support text extraction from the following MIME types:
    *   `application/pdf` (Native and Scanned)
    *   `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (DOCX)
    *   `text/plain` (TXT)
    *   `image/jpeg`, `image/png` (Images)
*   **FR3.2.3 (Hybrid Strategy):** For PDFs, the system SHALL first attempt native text extraction (e.g., via `pypdf`). If the extracted text density is too low (indicating a scan), it SHALL fallback to OCR.
*   **FR3.2.4:** The system SHALL use **Google Cloud Vision API** for OCR on images and scanned pages.
*   **FR3.2.5:** The system SHALL store the extracted text in the `documents` database table.
*   **FR3.2.6:** The system SHALL update the document status to `processing` when the job starts and `completed` (or `failed`) upon finish.
*   **FR3.2.7:** The system SHALL handle errors gracefully (e.g., OCR service down, corrupt file) by setting the status to `failed` and logging the error.

## 4. Acceptance Criteria (Gherkin)

### Scenario 1: Native PDF Extraction (Fast Path)
**Given** I have uploaded a native PDF document (text-selectable)
**When** the background worker processes the file
**Then** the text should be extracted using the local library (pypdf)
**And** the Google Cloud Vision API should **NOT** be called (cost optimization)
**And** the `extracted_text` field in the database should contain the document text
**And** the document status should update to `completed`

### Scenario 2: Scanned PDF/Image Extraction (OCR Path)
**Given** I have uploaded a scanned PDF or an image file (JPG/PNG)
**When** the background worker processes the file
**Then** the system should detect low text density (if PDF)
**And** it should call the Google Cloud Vision API to extract text
**And** the `extracted_text` field in the database should be populated with the OCR result
**And** the document status should update to `completed`

### Scenario 3: Asynchronous Workflow
**Given** a large document is queued for processing
**When** I query the document status API immediately after upload
**Then** I should receive a status of `pending` or `processing`
**And** the API request should return immediately (non-blocking)

### Scenario 4: Error Handling
**Given** a corrupt or unreadable file
**When** the worker attempts to process it
**Then** the processing should fail safely
**And** the document status should be set to `failed`
**And** the error should be logged for administrator review

## 5. Technical Implementation Details

### Architecture Components
*   **Queue:** Redis + RQ (Redis Queue) for job management.
*   **Worker:** Python worker process running `worker.py`.
*   **Services:**
    *   `OCRService`: Encapsulates logic for `pypdf`, `python-docx`, and `google-cloud-vision`.
    *   `DocumentService`: Handles DB updates.
*   **External API:** Google Cloud Vision API (requires `GOOGLE_APPLICATION_CREDENTIALS`).

### Database Schema Updates
Ensure `documents` table has:
*   `extracted_text` (Text/CLOB) - nullable.
*   `status` (Enum) - existing values: `pending`, `processing`, `completed`, `failed`.

### Dependencies
*   `pypdf`: For PDF parsing.
*   `python-docx`: For Word documents.
*   `google-cloud-vision`: For OCR.
*   `rq`: For background tasks.

## 6. Tasks & Subtasks

- [ ] **Setup & Configuration** (AC: All)
  - [ ] Add `google-cloud-vision`, `pypdf`, `python-docx`, `rq` to `backend/requirements.txt`.
  - [ ] Configure `GOOGLE_APPLICATION_CREDENTIALS` in `.env` and `docker-compose.yml`.
  - [ ] Setup Redis service in `docker-compose.yml` (if not already present from Story 1.5).

- [ ] **Implement OCR Service** (AC: 1, 2)
  - [ ] Create `backend/app/services/ocr_service.py`.
  - [ ] Implement `extract_from_pdf(path)` with density check and fallback logic.
  - [ ] Implement `extract_from_image(path)` using GCV.
  - [ ] Implement `extract_from_docx(path)`.
  - [ ] **Test:** Unit tests for `OCRService` (mocking GCV).

- [ ] **Implement Background Worker** (AC: 3)
  - [ ] Create/Update `backend/worker.py` to listen on `default` queue.
  - [ ] Implement `process_document(document_id)` task function.
  - [ ] Add logic to fetch document path, call `OCRService`, and update DB.
  - [ ] **Test:** Integration test ensuring job is enqueued and processed.

- [ ] **API Integration** (AC: 3)
  - [ ] Update `POST /api/v1/documents/` to enqueue `process_document` job after upload.
  - [ ] **Test:** Verify API returns 202 Accepted and job ID.

- [ ] **Error Handling & Logging** (AC: 4)
  - [ ] Add try/except blocks in worker task.
  - [ ] Ensure status is set to `failed` on exception.
  - [ ] Log full traceback.

## 7. Dev Notes

### Architecture Patterns
*   **Async Worker Pattern:** Strictly decouple the upload (HTTP Request) from processing (Worker). The API should only return "Accepted" and the ID.
*   **Service Layer:** Keep the extraction logic in `OCRService`, not in the worker function or API route.
*   **Cost Management:** The "density check" for PDFs is crucial to avoid unnecessary GCV costs. A simple heuristic is: `len(extracted_text) / num_pages > threshold`.

### Project Structure Alignment
*   Services go in `backend/app/services/`.
*   Worker entry point: `backend/worker.py`.
*   Tests: `backend/tests/services/test_ocr_service.py`.

### Learnings from Previous Story
**From Story 3.1 (Status: Ready for Dev)**
*   Story 3.1 set up the `documents` table and file storage. Ensure `process_document` task retrieves the correct file path using the UUID stored in the DB, not the original filename.
*   *Note: Detailed implementation learnings are not yet available as Story 3.1 is not fully completed.*

## 8. References
*   [Tech Spec Epic 3](./tech-spec-epic-3.md#story-32-ocr--text-extraction)
*   [Architecture: Async Processing](./architecture.md#21-high-level-data-flow)
*   [Google Cloud Vision API Docs](https://cloud.google.com/vision/docs/ocr)

## 9. Dev Agent Record

### Context Reference
*   **Story Context XML**: docs/story-3.2-ocr-for-scanned-documents.context.xml

### Agent Model Used
*   Gemini-2.5-Flash

### Debug Log References
*   None.

### Completion Notes List
*   (To be filled upon completion)

### File List
*   (To be filled upon completion)

### Completion Notes
**Completed:** 2025-12-09
**Definition of Done:** All acceptance criteria met, code reviewed, tests passing

## 10. Validation Notes

### Clarifications
*   **Source Coverage**: While aligned with the PRD and Test Design principles, these documents were not explicitly cited in the References section. Developers should refer to `docs/PRD.md` for business context and `docs/test-design.md` for broader testing strategies.