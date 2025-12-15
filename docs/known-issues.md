# Known Issues

## Testing
*   **E2E Tests:** The Playwright end-to-end tests (`npx playwright test`) require the backend and frontend servers to be running manually before execution.
    *   Backend: `uvicorn app.main:app --host 127.0.0.1 --port 8000` (from `backend/` with venv activated).
    *   Frontend: `npm run dev` (from `frontend/`).
    *   *Note:* The `playwright.config.ts` does not currently support `webServer` auto-start.

## Dashboard Test
*   **Skip:** The dashboard E2E test might be skipped or flaky due to mock data dependencies not being fully stubbed in the test environment.
