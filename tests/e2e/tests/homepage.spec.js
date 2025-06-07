const { test, expect } = require('@playwright/test');

test.describe('Homepage', () => {
  test('should load homepage successfully', async ({ page }) => {
    await page.goto('/');
    
    // Check page title
    await expect(page).toHaveTitle('React App');
    
    // Check main heading
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
    
    // Check main content
    await expect(page.getByText('This is the main dashboard area.')).toBeVisible();
    
    // Check sidebar navigation
    await expect(page.getByRole('menuitem', { name: /Users/ })).toBeVisible();
  });

  test('should have proper layout structure', async ({ page }) => {
    await page.goto('/');
    
    // Check that the layout has sidebar and main content
    // Use class selectors since Ant Design may not set ARIA roles consistently
    const sidebar = page.locator('.ant-layout-sider');
    await expect(sidebar).toBeVisible();
    
    const mainContent = page.locator('.ant-layout-content');
    await expect(mainContent).toBeVisible();
    
    // Check sidebar has dark theme menu
    const menu = page.locator('.ant-menu');
    await expect(menu).toBeVisible();
  });

  test('should be responsive', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Page should still be accessible on mobile
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
  });
}); 