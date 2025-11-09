# Brainstorm – Testing & QA Strategy (2025-11-09) — MVP aligned

## Goals
- Prevent regressions in parsing/OCR and JSON output
- Keep LLM generations consistent enough for demos & grading
- Fast feedback locally; smoke tests in CI (post-MVP)

## Pyramid
- **Unit**
  - Web: Vitest + Testing Library (components: FileCard, QuizItem, ResultRow)
  - API: Pytest (FastAPI routes, schema validation)
- **Integration**
  - API: Reader→Coach orchestration, JSON schema checks, error mapping (400/413/415/422/502)
- **E2E (smoke)**
  - Playwright: Upload → Processing → Quiz → Results; assert 5 MCQs, score calc, error banners

## LLM “Golden set”
- **Fixtures:** 3–5 sample docs with expected quiz JSON (stable ground truth)
- **Checks:** JSON parse, 5 items, unique options, valid source_span
- **Schedule:** run locally before PR; nightly smoke in CI (post-MVP)

## Contracts & validation
- **Reader→Coach contract v0**: jsonschema validation in orchestrator
- **Coach output**: backend validator
- **Quality gate:** block if `ocr_confidence < 0.85` or total text < 500 chars (422)

## Test data
- Text-only PDF
- Scanned PDF (good quality)
- Scanned PDF (blurry → fails gate)
- Non-English doc (blocked)
- Oversize file (21+ MB → 413)
- Corrupted/passworded PDF (400)
- LLM timeout simulation (force 502)

## Tooling & lint
- Web: ESLint + Prettier
- API: Ruff + Black
- Type-safe DTOs in TS + Pydantic models in Python

## CI/CD (post-MVP)
- GitHub Actions:
  1) Lint & unit
  2) API integration tests
  3) Playwright smoke (headless)
- Artifacts: test reports, coverage (informative only)

## Acceptance criteria (MVP)
- 100% of quiz responses are valid JSON
- Exactly 5 MCQs, all with valid `source_span`
- Error map enforced (400/413/415/422/502)
- Data purged on **Finish** or TTL