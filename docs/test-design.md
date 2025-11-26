# Test Design: AI Buddy (MVP)

**Project:** AI Buddy – IBE160 Student Project  
**Scope:** MVP (Single Persona "Student", Document Upload, AI Content Generation, Quiz/Flashcards)  
**Inputs:** `epics.md`, `PRD.md`, `ux-design-specification.md`, `architecture.md`  
**Status:** Draft (Pre-implementation)

---

## 1. Test Strategy

We adhere to the **Testing Pyramid** defined in `architecture.md`:

1.  **Unit Tests (Pytest/Jest):** High volume, fast. Cover individual functions, parsers, and isolated component logic.
    *   *Frontend:* Components (Buttons, Cards), Utils.
    *   *Backend:* Pydantic models, Utility functions (text cleaning), Agent logic (isolated).
2.  **Integration Tests (Pytest):** Medium volume. Cover API endpoints, Database interactions, and Agent-Orchestrator handoffs.
    *   *Focus:* `FastAPI` endpoints, `Redis` state management, `PostgreSQL` CRUD.
3.  **E2E Tests (Playwright):** Low volume, high value. Cover critical user journeys ("Golden Paths").
    *   *Focus:* Upload -> Study flow, Auth flow.

---

## 2. Test Scenarios by Epic

### Epic 1: Foundation & Core Setup
*Focus: Infrastructure health and CI pipeline.*

| ID | Scenario | Type | Location |
| :--- | :--- | :--- | :--- |
| **1.1** | **Backend Health Check**<br>**Given** the backend API is running<br>**When** I GET `/health`<br>**Then** I receive `200 OK` and status `{"status": "healthy"}` | Integration | `backend/tests/test_main.py` |
| **1.2** | **Frontend Smoke Test**<br>**Given** the frontend is running<br>**When** I visit the homepage<br>**Then** the page loads without crashing | E2E | `tests/e2e/smoke.spec.ts` |

### Epic 2: User Authentication & Onboarding
*Focus: Secure access and initial landing.*

| ID | Scenario | Type | Location |
| :--- | :--- | :--- | :--- |
| **2.1** | **User Registration (Happy Path)**<br>**Given** I am a new user on the Register page<br>**When** I enter a valid email and password<br>**Then** my account is created and I am redirected to Dashboard | E2E | `tests/e2e/auth.spec.ts` |
| **2.2** | **User Login (Happy Path)**<br>**Given** I have an existing account<br>**When** I login with correct credentials<br>**Then** I see my Dashboard | E2E | `tests/e2e/auth.spec.ts` |
| **2.3** | **Invalid Login (Edge Case)**<br>**Given** I am on the Login page<br>**When** I enter an incorrect password<br>**Then** I see an error message "Invalid credentials" | E2E | `tests/e2e/auth.spec.ts` |
| **2.4** | **Protected Route Redirect (Security)**<br>**Given** I am NOT logged in<br>**When** I try to visit `/dashboard`<br>**Then** I am redirected to `/login` | E2E | `tests/e2e/auth.spec.ts` |

### Epic 3: Document Processing & Analysis
*Focus: The "Reader" Agent and OCR pipeline.*

| ID | Scenario | Type | Location |
| :--- | :--- | :--- | :--- |
| **3.1** | **Upload Valid Document (Happy Path)**<br>**Given** I am on the Dashboard<br>**When** I upload a valid PDF (under 20MB)<br>**Then** the file is accepted and UI shows "Processing..." | E2E | `tests/e2e/upload.spec.ts` |
| **3.2** | **Upload Invalid File Type (Edge Case)**<br>**Given** I am on the Dashboard<br>**When** I upload a `.exe` file<br>**Then** the upload is rejected with error "Invalid file type" | E2E | `tests/e2e/upload.spec.ts` |
| **3.3** | **OCR Text Extraction (Integration)**<br>**Given** a mock scanned PDF file<br>**When** the `ReaderAgent` processes it<br>**Then** valid text content is extracted and stored in `ConversationContext` | Integration | `backend/tests/test_reader_agent.py` |
| **3.4** | **Large File Handling (Edge Case)**<br>**Given** a file > 20MB<br>**When** I attempt upload<br>**Then** the system rejects it gracefully | Unit/Int | `backend/tests/test_upload_limit.py` |

### Epic 4: AI-Powered Content Generation
*Focus: The "Coach" Agent and content creation.*

| ID | Scenario | Type | Location |
| :--- | :--- | :--- | :--- |
| **4.1** | **Generate Summary (Happy Path)**<br>**Given** a processed document context<br>**When** `CoachAgent` is triggered for "Summary"<br>**Then** a structured summary JSON is returned | Integration | `backend/tests/test_coach_agent.py` |
| **4.2** | **Generate Quiz (Happy Path)**<br>**Given** a processed document context<br>**When** `CoachAgent` is triggered for "Quiz"<br>**Then** a JSON with 5 multiple-choice questions is returned | Integration | `backend/tests/test_coach_agent.py` |
| **4.3** | **Quiz Schema Validation (Unit)**<br>**Given** raw LLM output<br>**When** parsed by the Quiz Parser<br>**Then** it validates: 5 questions, 4 options each, 1 correct answer | Unit | `backend/tests/test_parsers.py` |
| **4.4** | **Orchestrator Routing (Architecture)**<br>**Given** a user prompt "Give me a quiz"<br>**When** sent to Orchestrator<br>**Then** it routes to `CoachAgent` (not Reader) | Integration | `backend/tests/test_orchestrator.py` |

### Epic 5: Learning & Assessment
*Focus: Interactive UI for Quiz and Flashcards.*

| ID | Scenario | Type | Location |
| :--- | :--- | :--- | :--- |
| **5.1** | **Complete Quiz Flow (Happy Path)**<br>**Given** I have generated a quiz<br>**When** I answer all 5 questions<br>**Then** I see the Results card with my score | E2E | `tests/e2e/study.spec.ts` |
| **5.2** | **Flashcard Flip Interaction (UI)**<br>**Given** a flashcard is displayed<br>**When** I click the card<br>**Then** it flips to reveal the answer | Component | `frontend/src/tests/Flashcard.test.tsx` |
| **5.3** | **Quiz Immediate Feedback (UI)**<br>**Given** a quiz question<br>**When** I select the *wrong* answer<br>**Then** the button turns Red and the correct answer turns Green | E2E | `tests/e2e/study.spec.ts` |
| **5.4** | **Empty State Handling (Edge Case)**<br>**Given** the AI failed to generate questions<br>**When** I view the Quiz tab<br>**Then** I see a "Retry Generation" button, not a broken UI | E2E | `tests/e2e/study.spec.ts` |

### Epic 6: Basic Progress Tracking
*Focus: Dashboard and History.*

| ID | Scenario | Type | Location |
| :--- | :--- | :--- | :--- |
| **6.1** | **View Quiz History (Happy Path)**<br>**Given** I have completed 3 quizzes<br>**When** I visit the Dashboard<br>**Then** I see a list of 3 items with scores | E2E | `tests/e2e/dashboard.spec.ts` |
| **6.2** | **New User Dashboard (Empty State)**<br>**Given** I am a new user<br>**When** I visit the Dashboard<br>**Then** I see the "Start your first session" CTA | E2E | `tests/e2e/dashboard.spec.ts` |
| **6.3** | **Retake Quiz (Flow)**<br>**Given** an entry in History<br>**When** I click "Retake"<br>**Then** the Quiz interface loads with the *original* questions | E2E | `tests/e2e/dashboard.spec.ts` |

---

## 3. Summary of Coverage

### Covered
*   **Core Journey:** Upload -> Process -> Quiz -> Results (Full E2E coverage).
*   **Architecture:** Agent Orchestration and Handoff (Integration coverage).
*   **Safety:** Auth guards, File limits, Schema validation.

### Gaps / Future Work
*   **Performance Testing:** NFRs (load time < 3s) are not explicitly tested yet (post-MVP).
*   **LLM Hallucination:** Automated grading of *quality* of summaries (requires "Golden Set" evaluation dataset).
*   **Gamification:** Badges/Streaks logic is out of MVP scope (per `epics.md` note).

---

## 5. CI Pipeline

We have established a GitHub Actions pipeline (`.github/workflows/ci.yml`) to enforce quality gates on every push.

*   **Triggers:** Pushes to `main`, `feature/*`, and Pull Requests.
*   **Jobs:**
    1.  **Backend Test:** Installs Python dependencies and runs `pytest`.
    2.  **Frontend/E2E Test:** Installs Node dependencies, Playwright browsers, and runs `npm run test:e2e`.
*   **Strategy Alignment:** This pipeline ensures that both the Unit/Integration tests (Backend job) and critical User Journeys (E2E job) pass before merging code.

---

## 4. Next Steps (Implementation Order)

1.  **Scaffold Backend Tests:** Set up `backend/tests/conftest.py` with `pytest-asyncio` and `httpx`.
2.  **Scaffold Frontend Tests:** Configure `jest` or `vitest` for React components.
3.  **Implement Epic 1 & 2 Tests:** Verify infrastructure and Auth before building features.
4.  **Implement "Reader" Mock:** Create a mock Agent output to unblock Frontend E2E development before the real LLM is connected.
