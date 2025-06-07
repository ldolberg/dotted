/**
 * Authentication helper for Playwright tests
 */

/**
 * Authenticate via API and inject JWT token
 * @param {import('@playwright/test').Page} page 
 */
async function authenticateViaAPI(page) {
  console.log('🔐 Authenticating via API...');
  
  const baseURL = process.env.BASE_URL || 'http://frontend:3000';
  const apiURL = process.env.API_URL || 'http://backend:80';
  
  try {
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
    
    if (!response.ok()) {
      console.log('❌ API login failed with status:', response.status());
      const responseText = await response.text();
      console.log('Response:', responseText);
      throw new Error(`API login failed: ${response.status()}`);
    }
    
    const authData = await response.json();
    console.log('✅ API login successful');
    
    if (!authData.access_token && !authData.token) {
      console.log('❌ No token in response:', authData);
      throw new Error('No access token in API response');
    }
    
    const token = authData.access_token || authData.token;
    console.log('🎟️ Got JWT token');
    
    // Navigate to a page to set up the context
    await page.goto('/');
    
    // Inject the token into localStorage
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
      localStorage.setItem('authToken', token);
      localStorage.setItem('jwt_token', token);
      // Also try common variations
      localStorage.setItem('token', token);
      localStorage.setItem('auth_token', token);
    }, token);
    
    // Also set as a cookie in case the app uses cookies
    await page.context().addCookies([
      {
        name: 'access_token',
        value: token,
        domain: new URL(baseURL).hostname,
        path: '/',
        httpOnly: false,
        secure: false
      }
    ]);
    
    console.log('💾 Token injected into localStorage and cookies');
    
    // Navigate to homepage to verify authentication
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    return token;
    
  } catch (error) {
    console.log('❌ API authentication failed:', error.message);
    throw error;
  }
}

/**
 * Login to the application using demo credentials (UI fallback)
 * @param {import('@playwright/test').Page} page 
 */
async function loginViaUI(page) {
  console.log('🔐 Starting UI login process...');
  
  // Navigate to the login page (root URL redirects to login if not authenticated)
  await page.goto('/');
  console.log('📍 Navigated to root URL');
  
  // Wait for login form to be visible
  await page.getByRole('heading', { name: 'Welcome Back' }).waitFor({ timeout: 10000 });
  console.log('✅ Login form is visible');
  
  // Fill in the demo credentials
  console.log('📝 Filling credentials...');
  await page.getByRole('textbox', { name: /email/i }).fill('admin@test.com');
  await page.getByRole('textbox', { name: /password/i }).fill('admin123');
  
  // Click the Sign In button
  console.log('🖱️ Clicking Sign In button...');
  await page.getByRole('button', { name: 'Sign In' }).click();
  
  // Wait for navigation
  console.log('⏳ Waiting for response...');
  await page.waitForLoadState('networkidle', { timeout: 15000 });
  
  console.log('✅ UI login completed');
}

/**
 * Check if the user is already authenticated
 * @param {import('@playwright/test').Page} page 
 * @returns {Promise<boolean>}
 */
async function isAuthenticated(page) {
  try {
    // Check if we can see the dashboard layout (indicates authentication)
    await page.locator('.ant-layout-sider').waitFor({ timeout: 3000 });
    return true;
  } catch (error) {
    // Check if we're on the login page
    try {
      await page.getByRole('heading', { name: 'Welcome Back' }).waitFor({ timeout: 1000 });
      return false;
    } catch (error) {
      // Neither dashboard nor login page found, navigate to root to check
      return false;
    }
  }
}

/**
 * Setup authenticated page for tests
 * This will try API auth first, then UI fallback
 * @param {import('@playwright/test').Page} page 
 */
async function setupAuthenticatedPage(page) {
  // Navigate to homepage first to check if already authenticated
  await page.goto('/');
  
  // Check if we're already authenticated
  if (await isAuthenticated(page)) {
    console.log('✅ Already authenticated via storage state');
    return;
  }
  
  console.log('🔐 Not authenticated, attempting API authentication...');
  
  try {
    // Try API authentication first (faster and more reliable)
    await authenticateViaAPI(page);
    
    // Verify authentication worked
    if (await isAuthenticated(page)) {
      console.log('✅ API authentication successful');
      return;
    } else {
      throw new Error('API authentication completed but not authenticated');
    }
    
  } catch (error) {
    console.log('❌ API authentication failed, falling back to UI login:', error.message);
    
    try {
      // Fall back to UI login
      await loginViaUI(page);
      
      // Verify authentication worked
      if (await isAuthenticated(page)) {
        console.log('✅ UI authentication successful');
        return;
      } else {
        throw new Error('UI authentication completed but not authenticated');
      }
      
    } catch (uiError) {
      console.log('❌ Both API and UI authentication failed');
      throw new Error(`Authentication failed: API (${error.message}), UI (${uiError.message})`);
    }
  }
}

module.exports = {
  authenticateViaAPI,
  loginViaUI,
  setupAuthenticatedPage,
  isAuthenticated
}; 