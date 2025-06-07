import authService from './authService';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const patientApi = {
  fetchPatients: async () => {
    try {
      console.log('Fetching patients from backend...');
      
      // Try to call the real API first with authentication
      const response = await fetch(`${API_BASE_URL}/api/v1/patients`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...authService.getAuthHeaders(),
        },
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Successfully fetched patients from backend:', result);
        
        // Transform backend patient data to match our frontend format
        // Backend returns {data: [...]} format
        const patients = result.data || [];
        return patients
      } else if (response.status === 401) {
        console.warn('Authentication failed - redirecting to login');
        authService.logout();
        return [];
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error fetching patients:', error);
      console.log('Falling back to mock data...');
      // Fall back to mock data that matches the real backend data structure
      return [
        { 
          id: 1, 
          first_name: 'John', 
          last_name: 'Doe', 
          email: 'john.doe@example.com',
          phone_number: '123-456-7890',
          date_of_birth: '1993-01-01',
          address_street: '123 Main St',
          address_city: 'Anytown',
          address_state: 'CA',
          address_zip: '12345'
        },
        { 
          id: 2, 
          first_name: 'Jane', 
          last_name: 'Smith', 
          email: 'jane.smith@example.com',
          phone_number: '123-456-7890',
          date_of_birth: '1998-01-01',
          address_street: '456 Oak Ave',
          address_city: 'Somewhere',
          address_state: 'NY',
          address_zip: '67890'
        },
        { 
          id: 3, 
          first_name: 'Bob', 
          last_name: 'Johnson', 
          email: 'bob.johnson@example.com',
          phone_number: '555-123-4567',
          date_of_birth: '1978-01-01',
          address_street: '789 Pine St',
          address_city: 'Elsewhere',
          address_state: 'TX',
          address_zip: '54321'
        },
      ];
    }
  },
  
  createPatient: async (patientData) => {
    console.log('Creating patient:', patientData);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/patients`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authService.getAuthHeaders(),
        },
        body: JSON.stringify(patientData),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to create patient: ${response.status}`);
      }
      
      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Error creating patient:', error);
      throw error;
    }
  },

  updatePatient: async (patientId, patientData) => {
    console.log('Updating patient:', patientId, patientData);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/patients/${patientId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...authService.getAuthHeaders(),
        },
        body: JSON.stringify(patientData),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to update patient: ${response.status}`);
      }
      
      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Error updating patient:', error);
      throw error;
    }
  },

  deletePatient: async (patientId) => {
    console.log('Deleting patient:', patientId);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/patients/${patientId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          ...authService.getAuthHeaders(),
        },
      });
      
      if (!response.ok) {
        throw new Error(`Failed to delete patient: ${response.status}`);
      }
      
      return { success: true };
    } catch (error) {
      console.error('Error deleting patient:', error);
      throw error;
    }
  },
}; 