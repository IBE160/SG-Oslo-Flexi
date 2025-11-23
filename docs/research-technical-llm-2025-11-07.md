# Research – Technical: LLM Provider & Architecture Options for AI Buddy
**Date:** 2025-11-07  
**Project:** AI Buddy – The Multi‑Agent Learning Companion  
**Phase:** 1 – Analysis (BMAD)  
**Author:** Auto-generated

---

## 1) Scope & Objectives
Identify a practical, cost-aware, and secure AI stack for **summaries, flashcards, quizzes, and coaching** with a **multi‑agent** workflow. Compare options for:
- **Model provider / runtime** (hosted frontier models vs. local models)
- **Tooling & orchestration** (CLI/agents, MCP/tool-use, RAG)
- **Data & memory layer** (vector DB, auth, storage)
- **DX & deployment** (dev velocity, CI/CD, observability)

**Deliverable:** A recommendation for Phase 2 prototyping + a small validation plan.

---

## 2) Research Questions
1. Which model/runtime best supports **document summarization, key-point extraction, and Q&A** with consistent quality?
2. What’s the simplest way to implement **multi-agent orchestration** (orchestrator + 3–4 sub‑agents) without heavy infra?
3. How should we structure **RAG + memory** for user documents to keep context relevant and low-cost?
4. What data & privacy considerations must we satisfy for **student content** (notes, slides, recordings)?
5. What are the **must-have observability hooks** for debugging prompts and outputs?

---

## 3) Evaluation Criteria
- **Quality & Stability:** factual accuracy, determinism options, latency under 6–8s end-to-end
- **Multimodality:** text + PDF + (optional) audio transcription
- **Tool Use & RAG:** native function-calling / tool-use, easy integration with RAG
- **Cost Controls:** caching, rate limits, streaming, small-context fallbacks
- **DX (Developer Experience):** local dev story, CLI/SDKs, logging, prompt versioning
- **Privacy/Security:** PII controls, data retention options, regional hosting
- **Maintainability:** clear upgrade path, vendor lock-in mitigation
- **Licensing/Compliance:** education-friendly terms

Weights (suggested): Quality 30%, Cost 20%, DX 15%, Privacy 15%, Tooling 10%, Latency 10%.

---

## 4) Options Considered (High-Level)
### A) Hosted frontier model + CLI/agents + MCP + vector DB
- **Models:** modern general-purpose LLMs with strong reasoning & tool-use
- **Orchestration:** CLI/agents with **MCP** for file I/O, web fetch, RAG tools
- **Vector DB:** Supabase (Postgres + pgvector) for embeddings + auth + storage
- **Pros:** fastest path to a working multi-agent demo; rich tool ecosystem
- **Cons:** vendor dependency; usage-based cost; policies limit some data flows

### B) Hybrid: hosted model + lightweight server (Node/Next API routes)
- Frontend calls our API; server handles prompt routing, caching, and RAG
- **Pros:** flexible control of prompts, caching, guardrails; simple deploy on Vercel
- **Cons:** maintain our own API layer

### C) Local/On-device models (for privacy-first demos)
- Smaller open models w/ quantization
- **Pros:** strong privacy; no per-token cost
- **Cons:** lower quality; more engineering (tooling, RAG, GPU/CPU constraints)

**Conclusion:** For Phase 2, **Option A or B** offers the best quality/velocity trade-off.

---

## 5) Proposed Reference Architecture (MVP)
- **Frontend:** Next.js + React + Tailwind (SSR optional)
- **Agents:** Orchestrator + Analyzer + Flashcard + Quiz + Coach (prompt-chained)
- **Tooling:** MCP tools for file I/O, web fetch; RAG pipeline (embed → store → retrieve)
- **Data:** Supabase (Auth, Storage, Postgres/pgvector)
- **Observability:** request/response logging, prompt versions, latency metrics
- **Deployment:** Vercel (frontend & serverless API) + managed DB (Supabase)

---

## 6) RAG & Memory Design
- **Document pipeline:** upload → parse (text+metadata) → chunk (500–1000 tokens overlap 10–15%) → embed → store (pgvector)
- **Retrieval strategy:** top‑k (e.g., 6–12) + diversity (MMR) → compose **context window** with **structured sections**:
  - Task brief
  - Retrieved facts (with citations/IDs)
  - User preferences (from profile)
  - Output schema
- **Memory:**
  - **Short‑term:** per-session state for chat and task orchestration
  - **Long‑term:** embeddings for user docs; tables for progress & quiz results
- **Privacy baseline:** do not persist raw audio unless needed; store hashes for dedupe

---

## 7) Multi-Agent Orchestration (MVP)
**Flow:** Orchestrator → Analyzer → (Flashcard ∥ Quiz) → Coach → Orchestrator  
- **Analyzer:** extract outline, key points, glossaries, concept map
- **Flashcard:** convert key points → Q/A pairs; tag difficulty; spaced repetition fields
- **Quiz:** build MCQ + short-answer; include rationales; tag Bloom level
- **Coach:** synthesize plan (weak areas, suggested schedule), motivational nudge

**Guardrails:** schema validation (JSON), min/max lengths, citation fields, language codes (en/nb).

---

## 8) Prompting Strategy (Initial)
- **System prompts:** role, goal, constraints, schema
- **Task prompts:** explicit input→output contracts (JSON), few-shot exemplars
- **Self-check:** ask the model to verify: relevance, correctness, duplication, tone
- **Retry policy:** temperature=0 first; fallback small context; if failure → retry w/ tighter instructions

Example (Analyzer → Outline):
```json
{
  "goal": "Produce a hierarchical outline and 10 key takeaways from a lecture note.",
  "input": {"doc_excerpt": "...", "course": "IBE160"},
  "constraints": ["No hallucinations", "Quote exact phrases when possible"],
  "output_schema": {"outline": [], "key_takeaways": [], "citations": []},
  "quality_checks": ["Each takeaway <= 20 words", "At least 6 citations"]
}
```

---

## 9) Risks & Mitigations
- **Hallucinations:** RAG-first design; require citations; penalize unverifiable claims
- **Token bloat:** strict chunking; retrieval cap; compress summaries before handoff
- **Cost spikes:** caching; smaller models for flashcards; batch jobs off-peak
- **Latency:** parallelize Flashcard/Quiz; stream partial results to UI
- **Privacy:** limit PII; data retention policy; per-user encryption at rest
- **Vendor lock-in:** abstract model calls; store prompts & schemas in repo

---

## 10) Recommendation (Phase 2)
1. Build MVP with **hosted model + MCP tools + Supabase**.
2. Ship 4 agents under an Orchestrator with JSON schemas.
3. Implement RAG pipeline + vector search for user documents.
4. Add observability: logs, metrics, prompt versions.
5. Pilot with 2–3 real lecture note sets; collect feedback.

---

## 11) Validation Plan
- **Quality tests:** 10 doc sets → measure summary coverage, quiz correctness, flashcard clarity
- **UX tests:** 5 users run a 20‑min session → SUS score, task completion time
- **Cost/latency:** target p95 < 8s; estimate monthly cost @ 100 active students
- **Security review:** storage settings, retention policy, access controls

---

## 12) Action Items
- [ ] Set up Supabase (auth, storage, pgvector)
- [ ] Create embedding + retrieval scripts
- [ ] Implement Analyzer & Flashcard agents first
- [ ] Add Quiz & Coach with shared schemas
- [ ] Wire logs/metrics and prompt versioning
- [ ] Prepare demo dataset (3–5 lecture PDFs)
