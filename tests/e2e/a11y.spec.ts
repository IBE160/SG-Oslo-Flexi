import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Smoke Tests', () => {
  // Define the pages to test
  const pages = [
    { path: '/', name: 'Landing Page' },
    { path: '/login', name: 'Login Page' },
    { path: '/register', name: 'Register Page' },
  ];

  for (const pageInfo of pages) {
    test(`should pass a11y checks on ${pageInfo.name}`, async ({ page }) => {
      await page.goto(pageInfo.path);
      await page.waitForLoadState('domcontentloaded');
      const accessibilityScanResults = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
        .analyze();
      expect(accessibilityScanResults.violations).toEqual([]);
    });
  }

  test.skip('should pass a11y checks on Dashboard (after login)', async ({ page }) => {
    // 1. Register a new user
    const uniqueEmail = `test-user-${Date.now()}@example.com`;
    const password = 'Password123!';

    await page.goto('/register');
    await page.fill('input[type="email"]', uniqueEmail);
    await page.fill('input[type="password"]', password);
    await page.click('button[type="submit"]');

    // Wait for redirect to login (RegistrationForm has a 2s timeout)
    await page.waitForURL('**/login', { timeout: 10000 });

    // 2. Login
    await page.fill('input[type="email"]', uniqueEmail);
    await page.fill('input[type="password"]', password);
    await page.click('button[type="submit"]');

    // Wait for redirect to dashboard
    await page.waitForURL('**/dashboard', { timeout: 10000 });
    
    // Ensure content is loaded
    await page.waitForSelector('h1:has-text("Dashboard")');

    // 3. Run Axe
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });
});