# Brainstorm – Multi-Agent Handover (2025-11-09) — MVP aligned

## MVP principles
- **Single orchestrator (FastAPI)**; no external “agent runtime”. Roles (**Reader**, **Coach**) implementeres som interne services/funksjoner.
- **Synchronous path** end-to-end (no queues). One request → one response.
- **Versioned JSON contract** between Reader → Coach (`contract_version: "v0"`).
- **Traceability**: a `trace_id` is generated once and propagated through all logs and payloads.
- **Quality gate**: abort if OCR/text quality is too low or if no usable text exists.
- **Note**: Gemini CLI har **ikke** sub-agenter; all rolle-orkestrering skjer i FastAPI.

## Orchestrator flow (single endpoint)
1) **Client → POST** `/v0/generate-study-guide` with file (already validated for type/size/lang).
2) **Orchestrator**
   - Create `trace_id`.
   - Call **Reader** with `fileRef`.
3) **Reader**
   - Returns **Reader→Coach payload (v0)** (see schema below).
4) **Orchestrator**
   - Validate payload against JSON Schema.
   - Check quality gate (`ocr_confidence_score` and non-empty text).
   - If fail → **422** with actionable message.
5) **Orchestrator → Coach**
   - Send validated payload to **Coach**.
6) **Coach**
   - Returns study materials (quiz + optional flashcards).
7) **Orchestrator → Client**
   - `200 OK` with Coach output + `trace_id`.

## Reader → Coach JSON (v0)
Minimal, page-grounded text is the **source of truth**. Summaries/keywords are hints only.

```json
{
  "contract_version": "v0",
  "trace_id": "uuid",
  "doc_meta": {
    "filename": "lecture_notes.pdf",
    "filetype": "pdf",
    "pages": 15
  },
  "quality": {
    "ocr_confidence_score": 0.92,
    "unreadable_pages": [12]
  },
  "sections": [
    {
      "section_id": "page_1_para_1",
      "page_number": 1,
      "text": "The mitochondrion is a double-membraned organelle…"
    }
  ],
  "summary_bullets": [
    "Mitochondria generate ATP."
  ],
  "key_terms": ["Mitochondria", "ATP", "Cellular respiration"]
}
1```

### Coach output (v0)
Keep it small and consistent with Quiz Engine.

```json
{
  "trace_id": "uuid",
  "quiz_items": [
    {
      "itemType": "MCQ",
      "question": "Which organelle is known as the powerhouse of the cell?",
      "options": ["Nucleus", "Ribosome", "Mitochondrion"],
      "correctAnswerIndex": 2,
      "source_span": ["page_1_para_1"]
    }
  ],
  "flashcards": [
    {
      "front": "Primary role of the mitochondrion?",
      "back": "Generates ATP.",
      "source_span": ["page_1_para_1"]
    }
  ]
}
```

## JSON Schema (abridged) — validation at the orchestrator
> Use Pydantic or `jsonschema` to enforce shape.

```json
{
  "$id": "reader-coach-v0",
  "type": "object",
  "required": ["contract_version","trace_id","doc_meta","quality","sections"],
  "properties": {
    "contract_version": { "const": "v0" },
    "trace_id": { "type": "string" },
    "doc_meta": {
      "type": "object",
      "required": ["filename","filetype","pages"],
      "properties": {
        "filename": { "type": "string" },
        "filetype": { "enum": ["pdf","docx","pptx","txt","md"] },
        "pages": { "type": "integer", "minimum": 1 }
      }
    },
    "quality": {
      "type": "object",
      "required": ["ocr_confidence_score"],
      "properties": {
        "ocr_confidence_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "unreadable_pages": { "type": "array", "items": { "type": "integer", "minimum": 1 } }
      }
    },
    "sections": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["section_id","page_number","text"],
        "properties": {
          "section_id": { "type": "string" },
          "page_number": { "type": "integer", "minimum": 1 },
          "text": { "type": "string", "minLength": 1 }
        }
      }
    },
    "summary_bullets": { "type": "array", "items": { "type": "string" } },
    "key_terms": { "type": "array", "items": { "type": "string" } }
  }
}
```

## Quality gate (MVP)
- **Fail if** `ocr_confidence_score < 0.85` **or** total extracted text length < **N** (e.g., 500 chars).
- Response: **422 Unprocessable Entity**  
  `"Processing failed: document quality too low (confidence 0.63). Please try a clearer copy."`

## Errors (standardized)
- **400** Invalid contract (schema validation failed).
- **422** Quality gate failed / empty text.
- **502** LLM upstream error (Coach). Include `trace_id` and `stage: "coach_infer"`.

## Observability
- Every log line: `{ trace_id, stage, agent, duration_ms, status }`
- Stages: `upload`, `reader_infer`, `contract_validate`, `coach_infer`, `respond`
- Capture token usage (if available) under `coach_infer.tokens_total`
- Logs to stdout in JSON; central collector aggregates by `trace_id`.

## Non-goals (MVP)
- Async queues / PubSub / callbacks.
- Multi-turn agent feedback loops.
- Cross-document or RAG retrieval.
- Dynamic agent selection/routing. (Static: Reader→Coach.)

## Risks & mitigations
- **Schema drift** → versioned contract (`v0`), schema validation, backward-compat routes.
- **Reader quality varies** → gate on confidence & text length; show actionable errors.
- **Debugging complexity** → strict trace/log schema, fixed stages, single orchestrator.

## Decision
Keep **Reader→Coach** handover explicit and **schema-validated** under a **single, synchronous orchestrator** with strict quality gates and full traceability. Post-MVP can introduce async scaling, agent routing, and richer feedback loops.