const { test, expect } = require('@playwright/test');
const { setupAuthenticatedPage } = require('./auth.helper');

test.describe('Homepage', () => {
  test('should load homepage successfully', async ({ page }) => {
    // Login first
    await setupAuthenticatedPage(page);
    
    // Check page title
    await expect(page).toHaveTitle('React App');
    
    // Check main heading
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
    
    // Check main content
    await expect(page.getByText('This is the main dashboard area.')).toBeVisible();
    
    // Check sidebar navigation - verify both menu items exist
    await expect(page.getByRole('menuitem', { name: 'Dashboard' }).first()).toBeVisible();
    await expect(page.getByRole('menuitem', { name: 'Patients' }).first()).toBeVisible();
  });

  test('should have proper layout structure', async ({ page }) => {
    // Login first
    await setupAuthenticatedPage(page);
    
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
    
    // Login first
    await setupAuthenticatedPage(page);
    
    // Page should still be accessible on mobile
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
  });
}); 