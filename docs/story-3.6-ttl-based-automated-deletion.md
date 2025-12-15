# User Story 3.6: TTL-based Automated Deletion

**Epic:** [Epic 3: Document Processing & Analysis](./epics.md#epic-3-document-processing--analysis)
**Status:** Ready for Dev
**Sprint:** Sprint 3

## 1. User Story

**As a** system administrator,
**I want** documents and generated content to be deleted automatically after a set time (TTL),
**So that** system storage is kept clean, costs are managed, and user data is not retained indefinitely.

## 2. Context & Goal
To ensure data privacy and efficient resource usage, the system must not retain uploaded documents and their generated artifacts forever. This story introduces a "Time-To-Live" (TTL) mechanism that automatically identifies and purges expired data. This automated process acts as a safety net, complementing the manual deletion feature (Story 3.5), and ensures compliance with data retention policies (e.g., GDPR data minimization principles).

## 3. Functional Requirements

*   **FR3.6.1:** The system SHALL allow the TTL period to be configurable via an environment variable (e.g., `DOCUMENT_TTL_HOURS`), defaulting to 24 hours.
*   **FR3.6.2:** The system SHALL implement a background scheduled job (e.g., using `APScheduler` or `Celery` beat) that runs at a defined interval (e.g., every hour).
*   **FR3.6.3:** The scheduled job SHALL query the database for documents where the `created_at` timestamp is older than the defined TTL.
*   **FR3.6.4:** For each expired document found, the system SHALL execute the **exact same deletion logic** as defined in Story 3.5, ensuring:
    *   The physical file is removed from the storage volume.
    *   The document record is removed from the database.
    *   All associated generated content (summaries, flashcards, quizzes) are removed from the database (via cascading deletes).
*   **FR3.6.5:** The system SHALL log the number of documents deleted during each execution of the scheduled job for audit purposes.
*   **FR3.6.6:** If a deletion fails for a specific document, the job SHALL log the error and continue processing the remaining expired documents.

## 4. Acceptance Criteria (Gherkin)

### Scenario 1: Document Exceeds TTL
**Given** a document was uploaded 25 hours ago
**And** the `DOCUMENT_TTL_HOURS` is configured to 24
**And** the document file exists on the disk
**And** the document record exists in the database
**When** the automated cleanup job runs
**Then** the document record should be removed from the database
**And** the document file should be deleted from the disk
**And** the deletion count in the logs should increase by 1

### Scenario 2: Document Within TTL
**Given** a document was uploaded 23 hours ago
**And** the `DOCUMENT_TTL_HOURS` is configured to 24
**When** the automated cleanup job runs
**Then** the document record should REMAIN in the database
**And** the document file should REMAIN on the disk

### Scenario 3: Cascading Deletion Verification
**Given** an expired document has associated flashcards and a summary
**When** the automated cleanup job runs and deletes the document
**Then** the associated flashcards and summary records should also be removed from the database
**And** there should be no orphaned records linked to that document ID

### Scenario 4: Missing File Handling
**Given** an expired document record exists in the database
**But** the physical file has already been manually deleted from the disk (inconsistent state)
**When** the automated cleanup job runs
**Then** the system should safely remove the database record
**And** log a warning that the file was missing, but proceed without crashing

## 5. Constraints

*   **Logic Reuse:** MUST strictly reuse the deletion service/function implemented in Story 3.5 to avoid code duplication and ensure consistent behavior.
*   **Concurrency:** The job must handle potential race conditions if a user tries to manually delete a file at the exact moment the job is running (though highly unlikely, DB transactions should handle this).

## 6. Technical Implementation Details

### Architecture Components
*   **Scheduler:** Use `APScheduler` (Advanced Python Scheduler) integrated with the FastAPI application (or a separate worker process if preferred) to trigger the cleanup task.
*   **Configuration:** `settings.py` or `.env` loading for `DOCUMENT_TTL_HOURS` and `CLEANUP_INTERVAL_MINUTES`.
*   **Database:** Query `documents` table filtering by `created_at < (now - ttl)`.
*   **Service Layer:** Call `DocumentService.delete_document(doc_id)` (from Story 3.5) for each result.

### Data Model Impact
*   No schema changes required. Relies on the existing `created_at` timestamp in the `documents` table.

### Security & Privacy
*   **Data Minimization:** Directly supports privacy goals by ensuring data is not held longer than necessary.
*   **Logging:** Audit logs must not contain sensitive user data, only IDs and counts.

## 7. Non-Functional Requirements (NFRs)

*   **Reliability:** The scheduler must be robust and restart automatically if the application restarts.
*   **Performance:** The job should process deletions in batches if the volume is high, to avoid locking the database for long periods (though for MVP, simple iteration is acceptable).
*   **Observability:** Administrator should be able to verify from logs that the job is running and deleting files.

## 8. Dependencies
*   **Story 3.5 (Manual Deletion):** The deletion logic implementation is a hard dependency.
*   **Story 3.1 (File Upload):** `created_at` timestamp must be accurately recorded during upload.
*   **Story 1.5 (Background Job Queue):** While `APScheduler` can run in-app, using the existing Redis/RQ infrastructure for the actual deletion tasks is a valid alternative implementation strategy.

---

## 9. Validation Notes

### 9.1. Alignment Checks
*   ✅ **Epic 3:** Aligned with the goal of "Secure Temporary Storage" and automated maintenance.
*   ✅ **PRD:** Supports FR2.4: "The system SHALL delete uploaded documents... after a defined TTL".
*   ✅ **Project Brief:** Aligned with "Privacy: 'Delete data' on session; immediate purge".

### 9.2. Completeness
*   **Testable:** Scenarios cover expiration, non-expiration, and partial failure states.
*   **Safe:** Includes safeguards for missing files and error logging.
