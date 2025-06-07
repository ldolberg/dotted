// This is a placeholder patient API file
// Replace with actual API calls later

const mockPatients = [
  {
    id: '1',
    first_name: 'John Doe',
    last_name: 'Doe',
    dateOfBirth: '1990-05-15',
    email: 'john.doe@example.com',
    phone_number: '123-456-7890',
    address_street: '123 Main St',
    address_city: 'Anytown',
    address_state: 'CA',
    address_zip: '12345',
    // Add other patient fields as needed
  },
  {
    id: '2',
    first_name: 'Jane',
    last_name: 'Smith',
    dateOfBirth: '1985-11-20',
    email: 'jane.smith@example.com',
    phone_number: '123-456-7890',
    address_street: '123 Main St',
    address_city: 'Anytown',
    address_state: 'CA',
    address_zip: '12345',
    // Add other patient fields as needed
  },
];

const patientApi = {
  fetchPatientById: async (id: string) => {
    console.log(`Mock API: Fetching patient with id ${id}`);
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));
    const patient = mockPatients.find(p => p.id === id);
    if (!patient) {
      throw new Error('Patient not found');
    }
    return patient;
  },

  createPatient: async (patientData: any) => {
    console.log('Mock API: Creating patient', patientData);
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));
    // In a real scenario, you would send a POST request to your backend
    const newPatient = { id: Date.now().toString(), ...patientData }; // Generate a simple mock ID
    mockPatients.push(newPatient as any); // Add to mock data
    return newPatient;
  },

  updatePatient: async (id: string, patientData: any) => {
    console.log(`Mock API: Updating patient with id ${id}`, patientData);
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));
    // In a real scenario, you would send a PUT or PATCH request to your backend
    const index = mockPatients.findIndex(p => p.id === id);
    if (index === -1) {
      throw new Error('Patient not found');
    }
    mockPatients[index] = { ...mockPatients[index], ...patientData }; // Update mock data
    return mockPatients[index];
  },
};

export default patientApi; 