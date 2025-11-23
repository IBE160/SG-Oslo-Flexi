# Architecture: AI Buddy

## 1. Executive Summary

This document outlines the architecture for the AI Buddy MVP, a web-based learning assistant. The architecture is designed to be simple, scalable, and maintainable, prioritizing a clean separation of concerns between the frontend and backend. It uses a modern technology stack consisting of a Next.js frontend, a Python-based FastAPI backend, and a PostgreSQL database. A background worker system will handle long-running AI tasks, ensuring the user interface remains fast and responsive. All architectural decisions are in full compliance with the project proposal.

## 2. Guiding Principles

*   **Simplicity First:** For the MVP, we will always choose the simplest, most robust solution.
*   **Stateless, Pluggable Agents:** AI agents (Reader, Coach) will be built as independent tools that operate on a shared context, allowing for future scalability.
*   **Stateful Orchestration:** The system is designed with a future vision of a "Stateful Orchestrator" in mind, where a central service can dynamically route requests to specialist agents based on a shared conversation context.
*   **Traceability for Quality:** To combat compounding errors in the AI pipeline, all intermediate outputs (e.g., OCR text, summaries) must be logged to allow for debugging and quality control.

## 3. Project Initialization

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

| Category | Decision |
| :--- | :--- |
| **Data Persistence** | **PostgreSQL**, hosted on Railway. |
| **Authentication** | **NextAuth.js** using a **JWT-based** strategy. |
| **API Pattern** | **REST API** (via FastAPI) for all frontend-backend communication. |
| **File Storage** | **Local file storage** for the MVP; **Cloudflare R2** for production. |
| **Deployment Target** | **Vercel** for the Next.js frontend; **Railway** for the FastAPI backend and PostgreSQL database. |
| **Background Jobs** | **RQ (Redis Queue)** to handle long-running AI tasks asynchronously. Redis will be hosted on Railway. |
| **Email** | **Resend** for transactional emails, sent via the RQ background worker queue. |

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

---
_Generated by BMAD Decision Architecture Workflow_
