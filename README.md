# SG-Oslo-Flexi
Repository for SG-Oslo-Flexi - IBE160 Programmering med KI.

## Getting Started

### Prerequisites
- Node.js (v20+)
- Python (v3.10+)
- Poetry (v2.0+)

### Installation

#### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

#### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

## Development Workflow

### Accessibility Testing (WCAG 2.1 AA)
We use `axe-core` via Playwright to ensure our UI is accessible.

**To run accessibility tests locally:**
```bash
# Runs the full e2e suite including accessibility checks
npm run test:e2e
```

**What to expect:**
- The test suite scans key pages (Landing, Login, Register) for violations.
- A "Pass" means 0 critical or serious WCAG 2.1 AA violations.
- These tests run automatically in CI on every Push/PR.

**Note:** The *Dashboard* accessibility test is currently skipped in the automated suite due to test environment limitations (requires running backend), but the code is implemented for compliance.
