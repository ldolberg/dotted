const { test, expect } = require('@playwright/test');

test.describe('Navigation', () => {
  test('should navigate from homepage to patients page via URL', async ({ page }) => {
    // Start at homepage
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
    
    // Navigate to patients page
    await page.goto('/patients');
    await expect(page.getByRole('heading', { name: 'Patient List' })).toBeVisible();
  });

  test('should handle direct navigation to patients page', async ({ page }) => {
    // Go directly to patients page
    await page.goto('/patients');
    
    // Should load successfully
    await expect(page.getByRole('heading', { name: 'Patient List' })).toBeVisible();
    await expect(page.getByRole('table')).toBeVisible();
  });

  test('should handle direct navigation to homepage', async ({ page }) => {
    // Go directly to homepage
    await page.goto('/');
    
    // Should load successfully
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
    await expect(page.getByText('This is the main dashboard area.')).toBeVisible();
  });

  test('should maintain proper URLs during navigation', async ({ page }) => {
    // Go to homepage
    await page.goto('/');
    expect(page.url()).toMatch(/\/$|\/$/);
    
    // Go to patients
    await page.goto('/patients');
    expect(page.url()).toMatch(/\/patients$/);
  });

  test('should handle browser back/forward navigation', async ({ page }) => {
    // Start at homepage
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
    
    // Navigate to patients
    await page.goto('/patients');
    await expect(page.getByRole('heading', { name: 'Patient List' })).toBeVisible();
    
    // Go back
    await page.goBack();
    await expect(page.getByRole('heading', { name: 'Welcome to the Homepage' })).toBeVisible();
    
    // Go forward
    await page.goForward();
    await expect(page.getByRole('heading', { name: 'Patient List' })).toBeVisible();
  });

  test('should handle invalid routes gracefully', async ({ page }) => {
    // Try to navigate to non-existent route
    await page.goto('/nonexistent');
    
    // Should either show 404 or redirect to a valid page
    // For now, we'll just check it doesn't crash
    await page.waitForLoadState('networkidle');
    
    // The page should still be accessible (React Router should handle this)
    expect(page.url()).toContain('/nonexistent');
  });
}); 