const { test, expect } = require('@playwright/test');

test.describe('Patients Page', () => {
  test('should load patients page successfully', async ({ page }) => {
    await page.goto('/patients');
    
    // Check page title
    await expect(page).toHaveTitle('React App');
    
    // Check main heading
    await expect(page.getByRole('heading', { name: 'Patient List' })).toBeVisible();
    
    // Check table is present
    await expect(page.getByRole('table')).toBeVisible();
    
    // Check table headers
    await expect(page.getByRole('columnheader', { name: 'Name' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Age' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Diagnosis' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Action' })).toBeVisible();
  });

  test('should display patient data', async ({ page }) => {
    await page.goto('/patients');
    
    // Wait for data to load
    await page.waitForSelector('table tbody tr');
    
    // Check mock patient data is displayed
    await expect(page.getByRole('cell', { name: 'John Doe' })).toBeVisible();
    await expect(page.getByRole('cell', { name: '30' })).toBeVisible();
    await expect(page.getByRole('cell', { name: 'Flu' })).toBeVisible();
    
    await expect(page.getByRole('cell', { name: 'Jane Smith' })).toBeVisible();
    await expect(page.getByRole('cell', { name: '25' })).toBeVisible();
    await expect(page.getByRole('cell', { name: 'Cold' })).toBeVisible();
  });

  test('should have functional action buttons', async ({ page }) => {
    await page.goto('/patients');
    
    // Wait for table to load
    await page.waitForSelector('table tbody tr');
    
    // Test Edit button functionality
    const editButtons = page.getByRole('button', { name: 'Edit' });
    await expect(editButtons.first()).toBeVisible();
    await expect(editButtons.first()).toBeEnabled();
    
    // Test Delete button functionality
    const deleteButtons = page.getByRole('button', { name: 'Delete' });
    await expect(deleteButtons.first()).toBeVisible();
    await expect(deleteButtons.first()).toBeEnabled();
  });

  test('should handle button clicks', async ({ page }) => {
    // Listen for console logs to verify button click handlers
    const consoleLogs = [];
    page.on('console', msg => {
      if (msg.type() === 'log') {
        consoleLogs.push(msg.text());
      }
    });

    await page.goto('/patients');
    await page.waitForSelector('table tbody tr');
    
    // Click first Edit button
    await page.getByRole('button', { name: 'Edit' }).first().click();
    
    // Wait a bit for console log
    await page.waitForTimeout(100);
    
    // Verify console log was generated
    expect(consoleLogs.some(log => log.includes('Edit patient: 1'))).toBeTruthy();
    
    // Click first Delete button
    await page.getByRole('button', { name: 'Delete' }).first().click();
    
    // Wait a bit for console log
    await page.waitForTimeout(100);
    
    // Verify console log was generated
    expect(consoleLogs.some(log => log.includes('Delete patient: 1'))).toBeTruthy();
  });

  test('should have pagination', async ({ page }) => {
    await page.goto('/patients');
    
    // Check pagination is present
    await expect(page.locator('.ant-pagination, [role="navigation"]')).toBeVisible();
    
    // Check page number display
    await expect(page.getByText('1')).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/patients');
    
    // Page should still be accessible
    await expect(page.getByRole('heading', { name: 'Patient List' })).toBeVisible();
    await expect(page.getByRole('table')).toBeVisible();
  });
}); 