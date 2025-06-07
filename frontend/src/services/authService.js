const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

class AuthService {
  constructor() {
    this.tokenKey = 'auth_token';
    this.userKey = 'auth_user';
  }

  // Get stored token
  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  // Get stored user info
  getUser() {
    const userStr = localStorage.getItem(this.userKey);
    return userStr ? JSON.parse(userStr) : null;
  }

  // Store token and user info
  setAuthData(token, user = null) {
    localStorage.setItem(this.tokenKey, token);
    if (user) {
      localStorage.setItem(this.userKey, JSON.stringify(user));
    }
  }

  // Clear auth data
  clearAuthData() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
  }

  // Check if user is authenticated
  isAuthenticated() {
    const token = this.getToken();
    if (!token) return false;
    
    try {
      // Check if token is expired by decoding JWT (basic check)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Date.now() / 1000;
      return payload.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  // Login with email and password
  async login(email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Login failed');
      }

      // Store the token
      this.setAuthData(data.access_token);
      
      // Get user info after successful login
      const user = await this.getUserInfo();
      this.setAuthData(data.access_token, user);

      return { success: true, data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Register new user
  async register(email, password, name) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Registration failed');
      }

      return { success: true, data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Get user information using the stored token
  async getUserInfo() {
    const token = this.getToken();
    if (!token) return null;

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      console.error('Failed to get user info:', error);
      return null;
    }
  }

  // Logout
  logout() {
    this.clearAuthData();
    window.location.href = '/login';
  }

  // Get auth headers for API requests
  getAuthHeaders() {
    const token = this.getToken();
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  }
}

// Create singleton instance
const authService = new AuthService();
export default authService; 