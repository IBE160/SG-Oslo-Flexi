import { test, expect } from '@playwright/test';

test.describe('Document Deletion', () => {
  test('should allow a user to upload and then delete a document', async ({ page }) => {
    // 1. Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');

    // 2. Upload a document
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser'),
      page.click('button:has-text("Choose File")'),
    ]);
    await fileChooser.setFiles({
      name: 'test.txt',
      mimeType: 'text/plain',
      buffer: Buffer.from('this is a test file'),
    });
    await page.click('button:has-text("Upload")');
    
    // Wait for the document to appear in the list
    await expect(page.locator('text=test.txt')).toBeVisible({ timeout: 10000 });

    // 3. Delete the document
    const documentRow = page.locator('.flex.items-center.justify-between', { hasText: 'test.txt' });
    await documentRow.locator('button[aria-label="Delete document"]').click();

    // 4. Confirm deletion
    page.on('dialog', dialog => dialog.accept());
    
    // 5. Verify the document is gone
    await expect(page.locator('text=test.txt')).not.toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=No documents uploaded yet.')).toBeVisible();
  });
});
