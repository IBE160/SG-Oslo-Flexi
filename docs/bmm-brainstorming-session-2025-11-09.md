# Brainstorm – Core Features (2025-11-09) — MVP aligned

## Must-haves (MVP)
- **Upload a single document**, with validation:
  - Formats: **PDF, DOCX, PPTX, TXT, MD**
  - Language: **English only (MVP)**
  - Size: **≤ 20 MB**
- **OCR text extraction** for scans/images inside PDFs via **Google Cloud Vision**.
- **Ask questions** about the uploaded document; answers must be grounded **only** in that document.
- **Generate a simple quiz** (e.g., **5 multiple-choice** questions) with correct answer key and brief explanations.
- **Score & review**: user sees score and which answers were right/wrong.
- **Clear UI states**: Upload → Processing → Quiz → Results.
- **Error handling**: unsupported format/oversized file, OCR failure, or empty text.

## Should-haves
- Select specific sections of a document for quiz generation.
- Conversation & quiz history saved to user profile.
- More question types (true/false, short answer).
- Share/export quiz results.
- Let the user **review & edit extracted text** before quiz/Q&A.
- Additional languages and image uploads (PNG/JPG) beyond MVP.

## Dependencies (MVP)
- **OCR**: Google Cloud Vision (managed, accurate, fast).
- **LLM**: Gemini (Q&A and quiz generation).
- **Backend**: FastAPI (orchestration) + persistent storage for documents and results.
- **Frontend**: React-based SPA.
- **Note**: **No Vector DB/RAG in MVP** (see Post-MVP).

## Non-goals for MVP (explicit)
- **RAG / Vector Database** for retrieval over large corpora.
- **Multi-document** projects or cross-document reasoning.
- **Asynchronous background pipelines** (keep synchronous path for MVP; scale later).
- **Multi-agent “sub-agents”** (orchestrate roles inside FastAPI if needed, no separate agent runtime).

## Risks & mitigations
- **OCR inaccuracies** → use Cloud Vision; basic image pre-processing; allow post-OCR text review (Should-have).
- **LLM hallucination** → strict prompts that quote source spans; chunking + narrow context windows; add a small **golden set** of doc→QA pairs for regression checks.
- **Sluggish UX** → streaming responses where possible; clear progress indicators; upfront file validation.
- **Privacy** → encrypt at rest/in transit; short default retention; user-triggered delete/purge.

## Proposed decision
Focus MVP on the **single-document “upload → understand → quiz → score”** journey to validate the core value: turning static documents into interactive learning.