import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

// Load .env file
dotenv.config({ path: path.resolve(__dirname, '.env') });

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  // Global timeout: 60 seconds
  timeout: 60 * 1000,

  expect: {
    // Assertion timeout: 10 seconds
    timeout: 10 * 1000,
  },

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // Action timeout: 15 seconds
    actionTimeout: 15 * 1000,
    
    // Navigation timeout: 30 seconds
    navigationTimeout: 30 * 1000,
  },

  reporter: [
    ['html', { outputFolder: 'test-results/html', open: 'never' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['list']
  ],

  projects: [
    { 
      name: 'chromium', 
      use: { ...devices['Desktop Chrome'] } 
    },
    { 
      name: 'firefox', 
      use: { ...devices['Desktop Firefox'] } 
    },
    { 
      name: 'webkit', 
      use: { ...devices['Desktop Safari'] } 
    },
  ],

  outputDir: 'test-results/artifacts',

  webServer: [
    {
      command: 'cd frontend && npm run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: !process.env.CI,
      timeout: 120 * 1000,
      env: {
        ...process.env,
        NEXT_PUBLIC_API_URL: 'http://127.0.0.1:8000',
        NEXTAUTH_URL: 'http://localhost:3000',
        NEXTAUTH_SECRET: 'supersecret',
      },
    },
    {
      command: 'set DATABASE_URL=sqlite+aiosqlite:///./test.db && cd backend && .\\.venv\\Scripts\\python.exe -m alembic upgrade head && .\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --port 8000',
      url: 'http://127.0.0.1:8000',
      reuseExistingServer: !process.env.CI,
      timeout: 120 * 1000,
      env: {
        DATABASE_URL: 'sqlite+aiosqlite:///./test.db',
        ...process.env,
      }
    }
  ],
});
