import { Page } from '@playwright/test';

export class UserHelper {
  constructor(public page: Page) {}

  async createAndLoginUser() {
    // For now, we mock the login process or use a simplified flow
    // In a real scenario, this would register a new user via API and set the session cookie
    // OR go through the UI flow.
    
    // For MVP E2E against localhost, let's assume we can register via UI or API.
    // API is faster.
    
    const email = `testuser_${Date.now()}@example.com`;
    const password = 'password123';

    // 1. Register via API
    await this.page.request.post('http://localhost:8000/api/v1/users/register', {
      data: { email, password }
    });

    // 2. Login via UI to set NextAuth session
    await this.page.goto('/login');
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
    
    // 3. Wait for redirect
    await this.page.waitForURL('**/dashboard');
  }
}
