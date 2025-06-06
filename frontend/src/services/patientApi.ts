export const patientApi = {
  fetchPatients: async () => {
    // TODO: Implement actual API call
    console.log('Fetching patients...');
    // Return mock data for now
    return [
      { id: 1, name: 'John Doe', age: 30, diagnosis: 'Flu' },
      { id: 2, name: 'Jane Smith', age: 25, diagnosis: 'Cold' },
    ];
  },
  
  createPatient: async (patientData: any) => {
    console.log('Creating patient:', patientData);
    // TODO: Implement actual API call
    const response = await fetch('http://localhost:8000/patients', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    if (!response.ok) {
      throw new Error('Failed to create patient');
    }
    return response.json();
  },

  updatePatient: async (patientId: number, patientData: any) => {
    console.log('Updating patient:', patientId, patientData);
    // TODO: Implement actual API call
    const response = await fetch(`http://localhost:8000/patients/${patientId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    if (!response.ok) {
      throw new Error('Failed to update patient');
    }
    return response.json();
  },

  deletePatient: async (patientId: number) => {
    console.log('Deleting patient:', patientId);
    // TODO: Implement actual API call
    const response = await fetch(`http://localhost:8000/patients/${patientId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete patient');
    }
    return response.json();
  },
}; 