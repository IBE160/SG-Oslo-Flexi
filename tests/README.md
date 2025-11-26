# Test Infrastructure

This repository uses **Playwright** for End-to-End (E2E) testing.

## 🚀 Quick Start

1.  **Install dependencies**:
    ```bash
    npm install
    ```

2.  **Configure environment**:
    Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```

3.  **Run tests**:
    ```bash
    npm run test:e2e
    ```

## 📁 Directory Structure

```
tests/
├── e2e/                      # Test files (*.spec.ts)
├── support/                  # Framework infrastructure
│   ├── fixtures/             # Test fixtures (index.ts extends base test)
│   │   └── factories/        # Data factories (UserFactory, etc.)
│   └── helpers/              # Shared utility functions
└── README.md                 # This file
```

## 🛠 Architecture

### Fixtures & Factories
We use a **Fixture-First** approach. Do not put complex logic or API calls directly in tests. Use `fixtures` and `factories`.

*   **Factories** (`tests/support/fixtures/factories/`): generate valid data.
    *   Use `UserFactory` to create users.
    *   Factories handle **Auto-Cleanup** automatically.
*   **Fixtures** (`tests/support/fixtures/index.ts`): inject dependencies into tests.
    *   `userFactory`: injected into tests, cleans up after itself.

### Configuration
*   `playwright.config.ts`: Main config.
    *   **Timeouts**: Action (15s), Navigation (30s), Expect (10s), Test (60s).
    *   **Reporters**: HTML (local), JUnit (CI).
    *   **Artifacts**: Screenshot/Video/Trace only on failure/retry.

## 💡 Best Practices

1.  **Isolation**: Every test should run independently. Do not rely on state from previous tests.
2.  **Data**: Use `userFactory.createUser()` to get a fresh user. Never hardcode IDs or emails.
3.  **Selectors**: Use `data-testid` attributes (`page.getByTestId('submit-btn')`) over CSS classes.
4.  **Network-First**: If setting up data, use API calls in factories, not UI interactions.

## 🔍 Debugging

*   Run with UI mode: `npm run test:e2e:ui`
*   Show last report: `npm run test:e2e:report`
*   Debug mode: `npm run test:e2e:debug`
