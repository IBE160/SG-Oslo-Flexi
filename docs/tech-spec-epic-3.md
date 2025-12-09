# Technical Specification: Epic 3 - Document Processing & Analysis

**Status:** Draft
**Epic:** Epic 3 (Document Processing & Analysis)
**Sprint:** Sprint 3
**Author:** Scrum Master / Architect

---

## 1. Executive Summary
This epic implements the core document ingestion pipeline for AI Buddy. It covers the flow from a user uploading a file (PDF, DOCX, TXT) to the system extracting its text (via OCR or parsing) and the "Reader" agent generating an initial analysis. This pipeline is the foundation for all subsequent learning features (flashcards, quizzes).

**Key Technical Decisions:**
- **Asynchronous Processing:** File processing (especially OCR and LLM analysis) will be handled in the background using **Redis & RQ** to prevent blocking the HTTP request.
- **Storage:** Files will be stored in a **secured local volume** (mapped in Docker/Deployment) with unique IDs.
- **OCR:** Google Cloud Vision API will be used for scanned documents/images. `pypdf` or similar for native PDFs.
- **State Management:** The `documents` table in PostgreSQL will track the processing state (`uploading` -> `processing` -> `completed` | `failed`).

---

## 2. Architecture & Data Flow

### 2.1. High-Level Data Flow

1.  **Upload:** User sends file -> API (`POST /api/v1/documents/`) -> Server saves file to disk -> Creates DB record (Status: `uploading`).
2.  **Enqueue:** API pushes a job (`process_document`) to the Redis Queue -> Returns `202 Accepted` with `document_id`.
3.  **Processing (Worker):**
    *   Worker picks up job.
    *   **Text Extraction:**
        *   If image/scanned PDF -> Call **Google Cloud Vision API**.
        *   If native PDF/DOCX/TXT -> Use local libraries (`pypdf`, `python-docx`).
    *   **Analysis:**
        *   Worker sends extracted text to **LLM (Gemini)** with "Reader Agent" prompt.
        *   LLM returns Summary and Key Concepts.
    *   **Save:** Worker updates DB record with `extracted_text`, `summary`, and Status: `completed`.
4.  **Polling:** Frontend polls `GET /api/v1/documents/{id}` to check status.
5.  **Completion:** Frontend receives `completed` status and displays the summary.

### 2.2. Component Diagram

```mermaid
graph LR
    User[User (Frontend)] -->|Upload| API[FastAPI Backend]
    API -->|Save File| Storage[Local/Volume Storage]
    API -->|Create Record| DB[(PostgreSQL)]
    API -->|Enqueue Job| Redis[(Redis Queue)]
    
    Worker[RQ Worker] -->|Dequeue| Redis
    Worker -->|Read File| Storage
    Worker -->|OCR Request| GCV[Google Cloud Vision]
    Worker -->|Analyze| LLM[Gemini API]
    Worker -->|Update Record| DB
```

---

## 3. Database Schema

### 3.1. `documents` Table

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default: uuid4 | Unique document identifier. |
| `user_id` | UUID | FK -> `users.id` | Owner of the document. |
| `filename` | String | Not Null | Original filename (e.g., "lecture_notes.pdf"). |
| `file_path` | String | Not Null | Path to the stored file on disk. |
| `mime_type` | String | Not Null | e.g., `application/pdf`. |
| `file_size` | Integer | Not Null | Size in bytes. |
| `status` | Enum | 'pending', 'processing', 'completed', 'failed' | Current processing state. |
| `extracted_text`| Text | Nullable | Full text extracted from the document. |
| `summary` | Text | Nullable | AI-generated summary. |
| `created_at` | DateTime | Default: Now | Upload timestamp. |
| `updated_at` | DateTime | Default: Now | Last update timestamp. |

---

## 4. API Design

### 4.1. Upload Document
- **Endpoint:** `POST /api/v1/documents/`
- **Auth:** Required (Bearer Token).
- **Body:** `multipart/form-data` (`file`)
- **Response:**
    ```json
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "status": "pending",
      "filename": "notes.pdf"
    }
    ```

### 4.2. Get Document Status/Details
- **Endpoint:** `GET /api/v1/documents/{id}`
- **Auth:** Required. Owner check enforced.
- **Response:**
    ```json
    {
      "id": "...",
      "status": "completed",
      "summary": "This document covers...",
      "created_at": "..."
    }
    ```

### 4.3. Delete Document
- **Endpoint:** `DELETE /api/v1/documents/{id}`
- **Auth:** Required. Owner check enforced.
- **Response:** `204 No Content`

---

## 5. Implementation Details by Story

### Story 3.1: File Upload & Story 3.4: Secure Storage
*   **Backend:**
    *   Use `python-multipart` for handling uploads.
    *   Validate `content-type` (allow PDF, DOCX, TXT) and `content-length` (< 20MB).
    *   Generate a secure, random filename for storage to prevent directory traversal (e.g., use UUID as filename on disk).
    *   Store in a defined `UPLOAD_DIR` (configured via env var).
*   **Frontend:**
    *   Use a file upload component (e.g., drag & drop).
    *   Show upload progress bar.
    *   Handle error responses (file too large, invalid type).

### Story 3.2: OCR & Text Extraction
*   **Strategy:**
    *   **PDF:** Attempt to extract text using `pypdf`. If text density is low (scanned), fallback to OCR.
    *   **Images (JPG/PNG):** Direct OCR.
    *   **DOCX:** Use `python-docx`.
    *   **TXT:** Read directly.
*   **OCR Provider:** Google Cloud Vision API.
    *   Need `GOOGLE_APPLICATION_CREDENTIALS` in env.
    *   Service: `app.services.ocr_service.py` -> `extract_text_from_file(path)`.

### Story 3.3: "Reader" Agent Analysis
*   **Agent Logic:**
    *   This is a "Single-Shot" agent for the MVP (not a complex conversational loop yet).
    *   **Prompt:** "You are an expert academic tutor. Analyze the following text. Provide a concise summary (max 200 words) and a list of 5 key concepts."
    *   **Input:** Extracted text from Story 3.2.
    *   **Output:** JSON or structured text stored in `documents.summary`.
*   **Integration:**
    *   Service: `app.services.reader_agent.py` -> `analyze_text(text)`.

### Story 3.5: Deletion
*   **Hard Delete:**
    *   Remove record from `documents` table.
    *   Remove physical file from `UPLOAD_DIR`.
    *   (Future: cleanup vector embeddings if we had them).

---

## 6. Security Considerations

1.  **Malicious File Uploads:**
    *   Strictly validate MIME types using `python-magic` (don't trust the extension).
    *   Rename files upon saving to avoid executing malicious scripts.
    *   Limit file size to 20MB.
2.  **Access Control:**
    *   Every DB query for a document MUST filter by `user_id` from the JWT token.
    *   Files on disk should not be served via a public static URL. They are for internal processing only.
3.  **Data Privacy:**
    *   Users only see their own data.
    *   Deletion must be permanent.

## 7. Dependencies & Libraries

*   `python-multipart`: File upload handling.
*   `python-magic`: File type validation.
*   `pypdf`: PDF text extraction.
*   `python-docx`: Word doc extraction.
*   `google-cloud-vision`: OCR.
*   `rq`: Background task queue.
*   `google-generativeai` (or `openai`): LLM Client.

---

## 8. Validation Notes

### 8.1. Consistency Checks
- **Story Alignment:**
  - Story 3.1 (Upload): Covered (API `POST /api/v1/documents/`, `python-multipart`).
  - Story 3.2 (OCR): Covered (Hybrid approach: `pypdf` + Google Cloud Vision).
  - Story 3.3 (Reader Agent): Covered ("Single-Shot" prompt strategy).
  - Story 3.4 (Secure Storage): Covered (Local volume + UUID filenames + No public URL).
  - Story 3.5 (Deletion): Covered (Hard delete via API).
- **Architecture Alignment:**
  - Async Worker Pattern: Consistent with `docs/architecture.md` (Redis/RQ).
  - Database: Consistent (PostgreSQL).
  - Auth: Consistent (Bearer Token/JWT).

### 8.2. Gaps & Clarifications
- **Gap:** The automated "Time-To-Live" (TTL) deletion mentioned in Story 3.5 acceptance criteria ("...OR a defined TTL expires") is not explicitly architected.
  - *Recommendation:* Add a periodic background job (e.g., using `rq-scheduler` or a simple cron) to scan for and delete documents older than the TTL.
- **Clarification:** The tech spec mentions `documents.summary` as a text field. The "Reader" agent prompt asks for a "list of 5 key concepts" as well.
  - *Recommendation:* Store the result as structured JSON in the `summary` field (if using JSONB) or add a separate `key_concepts` column (JSONB or Text array) to the `documents` table to make it easier to display effectively on the frontend.
- **Clarification:** The "Stateful Orchestrator" concept from `docs/architecture.md` is mentioned as "Future Vision" in the tech spec, but the tech spec focuses on a "Single-Shot" agent. This is acceptable for the MVP but should be explicitly noted as a simplification for this Epic.

### 8.3. Risks
- **Risk:** Large file uploads (20MB) might time out on the server if not handled via streaming or proper timeout configurations in Gunicorn/Uvicorn.
- **Risk:** Google Cloud Vision API costs/quotas need to be monitored.

### 8.4. Action Items
1.  Add `key_concepts` column to the `documents` table schema.
2.  Add a note about implementing a daily `cleanup_job` for TTL enforcement.