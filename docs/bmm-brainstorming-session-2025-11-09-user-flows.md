# Brainstorm – User Flows (2025-11-09) — MVP aligned

## A) Happy path: Upload → Quiz → Results
1) **Upload file**
   - Validate client-side: type in [PDF, DOCX, PPTX, TXT, MD], size ≤ 20 MB
   - Show English-only banner
2) **Processing**
   - POST `/v0/generate-quiz` (FastAPI)
   - Server validates again; classify text vs image PDF
   - If image PDF → Cloud Vision OCR; else parse text
   - Quality gate: `ocr_confidence ≥ 0.85` and total text ≥ 500 chars
3) **Quiz**
   - Render 5 MCQs from Coach output (JSON)
   - User answers → Submit → Score
4) **Results**
   - Show score + per-item feedback (correct/incorrect, correct answer indicated)
   - CTA: **Start over** (purges session data)

## B) Error: Oversize file
- Detected at upload → block with “limit 20 MB” message
- No network call

## C) Error: Unsupported type
- Detected at upload/server → 415 with guidance to export as PDF/TXT

## D) Error: Low OCR quality
- After OCR: quality gate fails → 422 + banner with “try a clearer copy” + trace_id

## E) Error: LLM temporary failure
- Coach call times out / rate-limited → 502 + retry message + trace_id
- CTA: **Retry**

## F) Non-English document
- Detected in UI (explicit constraint) and/or backend → blocked with banner

## Data & lifecycle
- Temp storage; TTL 24h
- **Finish** clears all session data immediately

## Non-goals (MVP)
- Multi-file batches or cross-document reasoning
- Export/share results
- Multi-language processing