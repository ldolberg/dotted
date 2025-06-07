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
        const patients = await response.json();
        console.log('Successfully fetched patients from backend:', patients);
        
        // Transform backend patient data to match our frontend format
        return patients.map(patient => ({
          id: patient.id,
          name: `${patient.first_name} ${patient.last_name}`,
          age: patient.date_of_birth ? 
            new Date().getFullYear() - new Date(patient.date_of_birth).getFullYear() : 
            'Unknown',
          diagnosis: patient.email // Using email as placeholder since diagnosis is not in backend model
        }));
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
      // Fall back to mock data if API call fails
      return [
        { id: 1, name: 'John Doe (Offline)', age: 30, diagnosis: 'Flu' },
        { id: 2, name: 'Jane Smith (Offline)', age: 25, diagnosis: 'Cold' },
        { id: 3, name: 'Bob Johnson (Offline)', age: 45, diagnosis: 'Checkup' },
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