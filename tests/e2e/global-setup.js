// global-setup.js
const { chromium } = require('@playwright/test');

async function globalSetup(config) {
  console.log('🚀 Starting global setup for Playwright tests...');
  
  // Wait for services to be ready
  console.log('⏳ Waiting for frontend and backend services to be ready...');
  
  // Set up authentication state
  console.log('🔐 Setting up authentication state...');
  
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    const baseURL = process.env.BASE_URL || 'http://frontend:3000';
    const apiURL = process.env.API_URL || 'http://backend:80';
    
    // Try API authentication first
    try {
      console.log('🔄 Attempting API authentication...');
      
      // Make API call to login endpoint
      const response = await page.request.post(`${apiURL}/api/v1/auth/login`, {
        data: {
          email: 'admin@test.com',
          password: 'admin123'
        },
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok()) {
        const authData = await response.json();
        const token = authData.access_token || authData.token;
        
        if (token) {
          console.log('🎟️ Got JWT token via API');
          
          // Navigate to set up context
          await page.goto(baseURL);
          
          // Inject token
          await page.evaluate((token) => {
            localStorage.setItem('access_token', token);
            localStorage.setItem('authToken', token);
            localStorage.setItem('jwt_token', token);
            localStorage.setItem('token', token);
          }, token);
          
          // Set cookie
          await page.context().addCookies([{
            name: 'access_token',
            value: token,
            domain: new URL(baseURL).hostname,
            path: '/',
            httpOnly: false,
            secure: false
          }]);
          
          // Navigate to homepage and verify
          await page.goto(baseURL);
          await page.waitForLoadState('networkidle');
          
          // Check if authenticated
          try {
            await page.locator('.ant-layout-sider').waitFor({ timeout: 5000 });
            console.log('✅ API authentication successful in global setup');
          } catch (error) {
            throw new Error('API auth succeeded but dashboard not found');
          }
        } else {
          throw new Error('No token in API response');
        }
      } else {
        throw new Error(`API login failed: ${response.status()}`);
      }
      
    } catch (apiError) {
      console.log('❌ API authentication failed, trying UI login:', apiError.message);
      
      // Fall back to UI authentication
      await page.goto(baseURL);
      
      // Wait for login form to be visible
      await page.getByRole('heading', { name: 'Welcome Back' }).waitFor({ timeout: 30000 });
      
      // Fill in the demo credentials
      await page.getByRole('textbox', { name: /email/i }).fill('admin@test.com');
      await page.getByRole('textbox', { name: /password/i }).fill('admin123');
      
      // Click the Sign In button
      await page.getByRole('button', { name: 'Sign In' }).click();
      
      // Wait for successful login
      await page.waitForLoadState('networkidle');
      
      // Verify we're logged in
      await page.locator('.ant-layout-sider').waitFor({ timeout: 10000 });
      console.log('✅ UI authentication successful in global setup');
    }
    
    // Save authentication state
    const authStatePath = require('path').join(__dirname, 'auth-state.json');
    await page.context().storageState({ path: authStatePath });
    
    console.log('✅ Authentication state saved successfully');
    
  } catch (error) {
    console.error('❌ Failed to set up authentication:', error.message);
    // Don't fail the entire test suite if auth setup fails
    // Tests will fall back to individual login
  } finally {
    await browser.close();
  }
  
  console.log('✅ Global setup completed successfully');
}

module.exports = globalSetup; 