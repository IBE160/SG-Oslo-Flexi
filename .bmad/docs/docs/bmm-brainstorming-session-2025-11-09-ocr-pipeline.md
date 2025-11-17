# Brainstorm – OCR Pipeline (2025-11-09) — MVP aligned

## Scope (MVP)
- **Single-file ingest** per session.
- **Allowed formats:** PDF, DOCX, PPTX, TXT, MD.
- **Language:** English only (MVP).
- **Size limit:** ≤ **20 MB**.
- **OCR applies when needed:** 
  - If the file is **image-based** (e.g., scanned PDF), run OCR.
  - If the file is **text-based** (DOCX/PPTX/TXT/MD or texty PDF), do **pass-through** (no OCR).
- **Synchronous path:** Client → FastAPI → Storage (temp) → **Cloud Vision OCR** (if needed) → text payload → Client.
- **Output:** structured text **per page** with minimal metadata (page index, text, avg confidence).

## Processing flow (sync)
1) **Upload & validate** (type/size) → reject early on client + server.  
2) **Classify** file as text-based vs image-based PDF.  
3) **Extract**  
   - Text-based → parse text (no OCR).  
   - Image-based → **Cloud Vision** OCR.  
4) **Assemble result** `{ documentId, pages: [{pageIndex, text, avgConfidence}] }`.  
5) **Return** payload to Q&A/Quiz steps.

## Minimal output schema (MVP)
```json
{
  "documentId": "uuid",
  "pages": [
    { "pageIndex": 0, "text": "…", "avgConfidence": 0.93 },
    { "pageIndex": 1, "text": "…" }
  ]
}
```

## Quality gate & errors
- **Low confidence:** abort with specific message:  
  “Processing failed: document quality too low. Please try a clearer copy.”
- **Unsupported/oversize:** block with clear guidance (show limits in UI).
- **Empty text:** return explicit “No readable text found”.

## Non-goals (MVP)
- Direct **PNG/JPG** uploads (use PDF container instead).
- **Asynchronous** pipelines / queues.
- Bounding boxes / detailed layout mapping.
- Multi-document or cross-doc processing.
- Automatic language detection.

## Providers & ops
- **OCR:** **Google Cloud Vision** (managed, accurate, fast).  
- **Post-MVP fallback:** Tesseract in Cloud Run for cost control experiments.
- **Storage:** temp bucket with 24h lifecycle; encrypted in transit/at rest.
- **Observability:** structured logs + `trace_id` through the pipeline.

## Risks & mitigations
- **Accuracy on complex layouts:** start with simple, single-column docs; document limitations.
- **Latency:** keep flow sync; downsample extreme PDFs; strict size/page caps.
- **Cost:** managed OCR for MVP; evaluate hybrid (Vision/Tesseract) post-MVP.

## Decision
Keep the MVP pipeline **simple and synchronous** with **Cloud Vision OCR when needed**; everything else (PNG/JPG ingest, async queues, rich layout) is **post-MVP** to reduce complexity and align across docs.