# Brainstorm – Edge Cases & Failure Modes (2025-11-09) — MVP aligned

## Input / Ingestion
- **Allowed types (MVP):** `PDF, DOCX, PPTX, TXT, MD`  
  - **Reject** others with **415 Unsupported Media Type** and guidance in UI.  
- **Single file per session:** No multi-upload or image batches in MVP.  
- **Max size:** **≤ 20 MB** → **413 Payload Too Large** with clear hint to compress/export.  
- **Encrypted / password-protected PDFs:** **400 Bad Request** → “Password-protected files aren’t supported in MVP.”  
- **Corrupted / unreadable file:** **400 Bad Request** → “File appears corrupted; please export to PDF/TXT and retry.”  
- **(Optional cap)** Very long documents (e.g., >100 pages) may be **truncated** to first N pages with banner note.

## Processing (OCR & parsing)
- **Text-based docs (DOCX/PPTX/TXT/texty PDF):** Pass-through parsing (no OCR).  
- **Image-based PDFs:** OCR via **Cloud Vision**.  
- **Low OCR confidence:** Gate at **0.85** → abort with **422 Unprocessable Entity**:  
  “Processing failed: document quality too low. Please try a clearer copy.”  
- **Skew/rotation/low contrast:** No manual image pre-processing in MVP; Vision may auto-correct, but failures hit the 0.85 gate.  
- **Non-English content:** MVP is **English-only** → block with actionable message in UI.

## Generation (LLM / Coach) failures
- **Timeout / rate-limit / bad payload:** Catch, log `trace_id`, return **502** with friendly text:  
  “We couldn’t generate your quiz right now. Please try again in a few minutes.”  
- **Malformed LLM JSON:** Treat as upstream failure -> **502**; do not show stack traces.

## Output quality controls
- **Hallucinated `source_span`:** Prompt must enforce correct spans; discard items without valid spans (MVP rule).  
- **Duplicate questions:** Best-effort prompt instruction for diversity (no embedding pass in MVP).  
- **Tables/equations/layout heavy docs:** Treat as plain text; warn that fidelity may be reduced.

## Privacy & lifecycle
- **Ephemeral by default:** Delete upload + derivatives at **session end** or fixed **TTL (e.g., 1h)**, whichever first.  
- **No export/share in MVP:** Prevents accidental IP leakage; content remains in-session only.

## Standardized error map (MVP)
- **400** Invalid/unsupported state (password-protected, corrupted).  
- **413** Too large (>20 MB).  
- **415** Unsupported media type.  
- **422** Quality gate failed / no readable text.  
- **502** Upstream LLM/OCR service error.  
_All responses include `trace_id` and a user-friendly explanation._

## Acceptance checklist (dev/QA)
- Upload: wrong type → 415 with UI hint.  
- Upload: 21 MB → 413 with limit shown.  
- Non-English doc → blocked with English-only banner.  
- Blurry scan → 422 (confidence < 0.85).  
- LLM timeout → 502 with retry message.  
- Quiz items: each has valid `source_span`; no identical duplicates in top-5.  
- Data purged when user clicks **Finish** or TTL elapses.

## Decision
Keep the MVP strict and predictable: one file, small set of formats, English-only, sync pipeline with clear gates and human-readable errors; defer multi-image ingest, fallbacks, and de-dup embeddings to post-MVP.