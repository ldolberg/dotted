import axios from 'axios';

// Create an instance of axios with a base URL
const instance = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // This should match your backend API base URL
  timeout: 5000, // Request timeout
  headers: {
    'Content-Type': 'application/json',
    // If your API requires authentication, you might need to add a token here.
    // For example:
    // 'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  },
});

export default instance; 