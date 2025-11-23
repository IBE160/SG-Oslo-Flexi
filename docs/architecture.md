# Architecture: AI Buddy

## 1. Executive Summary

This document outlines the architecture for the AI Buddy MVP, a web-based learning assistant. The architecture is designed to be simple, scalable, and maintainable, prioritizing a clean separation of concerns between the frontend and backend. It uses a modern technology stack consisting of a Next.js frontend, a Python-based FastAPI backend, and a PostgreSQL database. A background worker system will handle long-running AI tasks, ensuring the user interface remains fast and responsive. All architectural decisions are in full compliance with the project proposal.

## 2. Guiding Principles

*   **Simplicity First:** For the MVP, we will always choose the simplest, most robust solution.
*   **Stateless, Pluggable Agents:** AI agents (Reader, Coach) will be built as independent tools that operate on a shared context, allowing for future scalability.
*   **Stateful Orchestration:** The system is designed with a future vision of a "Stateful Orchestrator" in mind, where a central service can dynamically route requests to specialist agents based on a shared conversation context.
*   **Traceability for Quality:** To combat compounding errors in the AI pipeline, all intermediate outputs (e.g., OCR text, summaries) must be logged to allow for debugging and quality control.

## 3. Project Initialization

*(This section also implicitly defines decisions fulfilled by our chosen starter templates, such as the testing framework and initial file structure.)*

The project will be set up as a monorepo with two primary packages: `frontend` and `backend`.

### Frontend Setup (Next.js)

```bash
# 1. Create the Next.js application
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir

# 2. Navigate into the new directory
cd frontend

# 3. Initialize Shadcn/UI for our component library
npx shadcn-ui@latest init
```

### Backend Setup (FastAPI)

```bash
# From the project root
mkdir backend
cd backend

# 1. Initialize a new Python project with Poetry
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry init --name "ai-buddy-backend" --python "^3.10" -n
poetry add fastapi "uvicorn[standard]" python-dotenv

# 2. Create initial project structure
mkdir -p app/api services workers core tests
touch app/__init__.py app/main.py
```

## 4. Architecture Decision Records (ADRs)

| Category | Decision | Version |
| :--- | :--- | :--- |
| **Data Persistence** | **PostgreSQL**, hosted on Railway. | 18.1 |
| **Authentication** | **NextAuth.js** using a **JWT-based** strategy. | 4.24.13 |
| **API Pattern** | **REST API** (via FastAPI on Python) | FastAPI: 0.121.3, Python: 3.10.19 |
| **File Storage** | **Local file storage** for the MVP; **Cloudflare R2** for production. | N/A |
| **Deployment Target** | **Vercel** for the Next.js frontend; **Railway** for the backend. | Next.js: 16 |
| **Background Jobs** | **RQ (Redis Queue)** on Redis. | RQ: 2.6.0, Redis: 8.4 |
| **Email** | **Resend** for transactional emails, sent via the RQ background worker queue. | 2.19.0 |

## 5. Cost & Free Tiers (Hobby/Starter Plans)

This architecture is designed to be extremely cost-effective, with a likely cost of **$0** during development and initial testing.
*   **Vercel (Frontend):** *Free.* Includes 100 GB of bandwidth, 1,000,000 function invocations, and 100 hours of build time per month.
*   **Railway (Backend & DB):** *Free.* Includes a $1 monthly credit, 0.5 GB RAM, and 0.5 GB of database storage, which is sufficient for initial development.
*   **Cloudflare R2 (Storage):** *Free.* Includes 10 GB of storage and 10 million read operations per month with zero egress fees.
*   **Resend (Email):** *Free.* Includes 3,000 emails per month (100 per day).

## 6. Project Structure

```
/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── workers/
│   │   └── core/
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   ├── tests/
│   └── package.json
├── docs/
└── README.md
```

## 7. Implementation Patterns & Style Guide

A comprehensive style guide will be enforced by automated tooling to ensure consistency.
*   **General:** All new code must be accompanied by tests. All developers must use editor integrations for Prettier/Black to format code on save.
*   **Git:** Branches will be named `feature/...` or `bugfix/...`. Commits will follow the Conventional Commits standard (e.g., `feat: ...`, `fix: ...`).
*   **Database Naming:** Tables and columns will be `snake_case`. Tables will be plural (e.g., `users`).
*   **API Naming:** JSON fields will be `snake_case`. API endpoints will be resource-oriented (e.g., `/documents`).
*   **Frontend Naming:** Component files will be `PascalCase` (`QuizDisplay.tsx`). Variables will be `camelCase`.
*   **Environment Vars:** `UPPER_SNAKE_CASE`. Browser-exposed variables must be prefixed with `NEXT_PUBLIC_`.

## 8. Cross-Cutting Concerns

*   **Error Handling:** The REST API will use a standard error format for all failed requests: `{ "error": { "message": "...", "code": "..." } }`.
*   **Success Responses:** All successful API responses will be wrapped in a `data` object: `{ "data": { ... } }`.
*   **Logging:** All application logs will be structured JSON to enable fast searching and analysis.
*   **Date/Time:** All timestamps on the backend/database will be in **UTC**. Timestamps in the API will be **ISO 8601** strings. The frontend is responsible for converting to local time.
*   **Testing:** We will use the "Testing Pyramid" strategy: many **Unit Tests** (Pytest, Jest), some **Integration Tests**, and a few **End-to-End Tests**.

## 9. Novel Patterns

This section details custom architectural patterns designed specifically for the AI Buddy platform to ensure scalability and maintainability.

### Stateful Orchestrator

**Purpose:** The Stateful Orchestrator is a central backend service that manages the lifecycle of a user's interaction. It maintains the conversation state and routes requests to the appropriate specialist AI agent (e.g., Reader, Coach) based on the current context. This decouples the frontend from the individual AI agents and allows new agents to be added with minimal friction.

**Component Interactions:**

1.  **Frontend -> Orchestrator:** The frontend makes all its requests to a single endpoint on the Orchestrator (e.g., `POST /api/v1/orchestrator/`). The request body contains the `session_id` and the user's `prompt`.
2.  **Orchestrator -> State Store (Redis):** The Orchestrator retrieves the current conversation `context` from Redis using the `session_id`.
3.  **Orchestrator -> Specialist Agent:** The Orchestrator analyzes the `prompt` and the `context` to determine which specialist agent to call. It then calls the specialist agent's internal API (e.g., `POST /agents/reader/process`), passing the relevant context.
4.  **Specialist Agent -> Orchestrator:** The specialist agent performs its task and returns the result, including any updates to the context.
5.  **Orchestrator -> State Store (Redis):** The Orchestrator updates the conversation `context` in Redis with the new information.
6.  **Orchestrator -> Frontend:** The Orchestrator returns the final result to the frontend.

**Data Flow & State Management:**

The core of the orchestrator is the `ConversationContext` object, stored in Redis as a JSON blob against a `session_id` key.

*   **Example `ConversationContext` Object:**
    ```json
    {
      "session_id": "user123_abc",
      "history": [
        { "role": "user", "content": "Analyze this document for me." },
        { "role": "assistant", "content": "Okay, I have read the document. What would you like to know?" }
      ],
      "current_document": {
        "id": "doc_xyz",
        "raw_text": "The quick brown fox...",
        "summary": "A sentence about a fox."
      },
      "last_agent_used": "Reader"
    }
    ```

*   **Sequence:**
    1.  User sends a prompt.
    2.  Orchestrator fetches the `ConversationContext`.
    3.  A simple routing rule is applied: If the prompt contains "read" or "analyze document", route to `ReaderAgent`. If it contains "quiz me" or "ask me questions", route to `CoachAgent`.
    4.  The chosen agent receives the `ConversationContext`.
    5.  The agent returns a `result` and a `new_context_state` object.
    6.  The Orchestrator merges the `new_context_state` into the `ConversationContext` in Redis and sends the `result` to the user.

**Implementation Guide for New Agents:**

To add a new specialist agent (e.g., a `SummarizerAgent`):

1.  Create a new service that exposes a single endpoint (e.g., `/agents/summarizer/process`).
2.  The endpoint must accept a `ConversationContext` object.
3.  The agent's logic reads from the context, performs its function, and returns a JSON object containing `result` and `new_context_state`.
4.  Register the agent and its trigger keywords (e.g., "summarize") in the Orchestrator's routing table.

---
_Generated by BMAD Decision Architecture Workflow_
