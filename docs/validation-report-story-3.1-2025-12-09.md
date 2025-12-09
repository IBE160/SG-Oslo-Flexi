# Test Review: Story 3.1 - File Upload

**Date:** 2025-12-09
**Reviewer:** Tea (Test Engineering Analyst)
**Scope:** `backend/tests/test_upload_document.py`, `tests/e2e/upload.spec.ts`
**References:** `docs/story-3.1-file-upload.md`, `docs/tech-spec-epic-3.md`

## 1. Executive Summary
The test suite provides a foundational coverage of Story 3.1, addressing the core "happy path" (valid upload) and basic security checks (unauthorized access, invalid file types). However, there are significant gaps in backend validation for file size and "masked" file types (security), and the E2E negative test cases are incomplete.

**Verdict:** **Acceptable with Reservations.** The current suite verifies the critical success path, but **Must Fix** items below should be addressed before declaring the story "Done" to ensure security and robustness.

## 2. Detailed Coverage Analysis

### 2.1 Backend Tests (`backend/tests/test_upload_document.py`)
*   **✅ Strengths:**
    *   **Auth Integration:** Correctly tests protected endpoints using `create_user_and_get_token` (covers Story 2.4 dependency).
    *   **Happy Path:** `test_upload_document_success` verifies status `202`, `pending` state, and filename persistence.
    *   **Security:** `test_upload_unauthorized` ensures non-logged-in users cannot upload.
    *   **Type Validation:** `test_upload_invalid_file_type` checks for explicit executable file rejections.

*   **⚠️ Gaps & Weaknesses:**
    *   **Missing Size Limit Test (FR3.1.3):** There is NO backend test verifying that a file > 20MB is rejected. This is a critical security/resource control requirement. Relying solely on frontend validation is insufficient.
    *   **"Masked" File Type Test (FR3.1.4):** The current test uses a `.exe` extension. The story explicitly requires preventing "executables masked as PDFs". A test case uploading a file named `safe.pdf` with `MZ` (executable) headers is missing to verify `python-magic` is actually inspecting content, not just extensions.

### 2.2 E2E Tests (`tests/e2e/upload.spec.ts`)
*   **✅ Strengths:**
    *   **User Flow:** Simulates the real user journey from Dashboard -> File Selection -> Upload.
    *   **Client-Side Validation:** `should reject file too large` verifies the immediate UI feedback for large files.

*   **⚠️ Gaps & Weaknesses:**
    *   **Auth/Registration Instability:** As noted, these tests currently fail or are flaky due to underlying auth/registration flow issues in the test environment (Story 2.1/2.4).
    *   **Incomplete Negative Scenarios:** The `should reject invalid file type` test contains comments indicating it is not fully implemented ("Let's assume..."). It needs to verify that the dropzone actually rejects the file or shows an error message.

## 3. Improvement Recommendations

### High Priority (Security & Compliance)
1.  **Add Backend Size Test:** Create a test in `test_upload_document.py` that attempts to upload a mock file slightly larger than 20MB (can use a generator to avoid creating a large file in memory if the client supports streaming, or just a large byte string if memory allows) and asserts a `413 Request Entity Too Large` or `400 Bad Request`.
2.  **Add "Masked" Type Test:** Add a backend test case:
    ```python
    files = {"file": ("fake_report.pdf", b"MZ...", "application/pdf")}
    # Expect 400 Error due to mime-type mismatch/detection
    ```

### Medium Priority (Robustness)
3.  **Fix E2E Auth Helper:** Stabilize the `UserHelper` class to ensure `createAndLoginUser` is reliable, possibly by mocking the auth response if the full backend flow is not the target of this specific test (though full integration is preferred).
4.  **Implement E2E Invalid Type Test:** Finish the `should reject invalid file type` test in Playwright to assert that the file is not added to the `acceptedFiles` list or that a specific error toast appears.

## 4. Conclusion
The testing foundation is solid enough to proceed with development of dependent stories (like OCR), provided the **High Priority** backend tests are added immediately to secure the upload endpoint. The E2E instability is a known infrastructure issue that should be tracked separately.