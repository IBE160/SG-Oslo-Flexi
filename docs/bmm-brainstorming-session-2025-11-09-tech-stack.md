# Brainstorm – Tech Stack (2025-11-09) — MVP aligned with course

> Aligned with IBE160 examples: **Gemini CLI** for local prompting, **Next.js** front-end, **FastAPI** orchestration, **Cloud Vision** OCR, synchronous MVP.

## Frontend
- **Framework:** Next.js (App Router), TypeScript, React 18
- **UI:** TailwindCSS + shadcn/ui
- **State:** React Query (server data), minimal local state
- **Build/Dev:** Vite (via Next.js under the hood) or default Next tooling
- **Hosting:** Vercel (preview deployments for PRs)
- **Why (course-aligned):** Next.js + Vercel are used in examples and fit rapid MVP demos.

## Backend (orchestrator)
- **Runtime:** Python 3.11, **FastAPI** + Uvicorn
- **Validation:** Pydantic v2 + `jsonschema` for contract checks
- **LLM access:** Gemini API (Gemini CLI for local prompt iteration)
- **Deploy:** Google Cloud Run (containerized), HTTPS only
- **Config:**