// Patient Data Service
// This service handles both real database connections and fallback mock data

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001/api';

// Check if real API is available
const checkAPIAvailability = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      timeout: 3000, // 3 second timeout
    });
    return response.ok;
  } catch (error) {
    console.log('API not available, using mock data');
    return false;
  }
};

// Fetch patients from real API
const fetchPatientsFromAPI = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/patients`);
    if (!response.ok) {
      throw new Error('Failed to fetch patients');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching patients from API:', error);
    throw error;
  }
};

// Create patient via API
const createPatientAPI = async (patientData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/patients`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    if (!response.ok) {
      throw new Error('Failed to create patient');
    }
    return await response.json();
  } catch (error) {
    console.error('Error creating patient:', error);
    throw error;
  }
};

// Update patient via API
const updatePatientAPI = async (patientId, patientData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    if (!response.ok) {
      throw new Error('Failed to update patient');
    }
    return await response.json();
  } catch (error) {
    console.error('Error updating patient:', error);
    throw error;
  }
};

// Delete patient via API
const deletePatientAPI = async (patientId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete patient');
    }
    return true;
  } catch (error) {
    console.error('Error deleting patient:', error);
    throw error;
  }
};

// Fallback mock data - minimal single patient
const getMockPatients = () => {
  return [
    {
      id: 1,
      nameKey: '1', // Reference to translation key
      name: 'Amit Sharma', // Fallback name
      age: 42,
      gender: 'Male',
      condition: 'Paralysis',
      status: 'Active',
      phone: '+91 98765 43210',
      address: 'Delhi, India',
      dateAdmitted: '2025-07-15',
      treatmentPlan: 'Physiotherapy sessions 3x/week',
      emergencyContact: '+91 98765 43211',
      bloodType: 'O+',
      allergies: 'None',
      medications: 'Aspirin, Physiotherapy aids',
    }
  ];
};

// Main service class
export class PatientService {
  constructor() {
    this.apiAvailable = null;
    this.mockData = getMockPatients();
  }

  // Initialize service - check API availability
  async initialize() {
    if (this.apiAvailable === null) {
      this.apiAvailable = await checkAPIAvailability();
    }
    return this.apiAvailable;
  }

  // Get all patients
  async getPatients() {
    await this.initialize();
    
    if (this.apiAvailable) {
      try {
        return await fetchPatientsFromAPI();
      } catch (error) {
        console.warn('API failed, falling back to mock data');
        this.apiAvailable = false;
        return this.mockData;
      }
    } else {
      return this.mockData;
    }
  }

  // Create new patient
  async createPatient(patientData) {
    await this.initialize();
    
    if (this.apiAvailable) {
      try {
        return await createPatientAPI(patientData);
      } catch (error) {
        console.warn('API failed, falling back to mock mode');
        this.apiAvailable = false;
        return this.createPatientMock(patientData);
      }
    } else {
      return this.createPatientMock(patientData);
    }
  }

  // Update patient
  async updatePatient(patientId, patientData) {
    await this.initialize();
    
    if (this.apiAvailable) {
      try {
        return await updatePatientAPI(patientId, patientData);
      } catch (error) {
        console.warn('API failed, falling back to mock mode');
        this.apiAvailable = false;
        return this.updatePatientMock(patientId, patientData);
      }
    } else {
      return this.updatePatientMock(patientId, patientData);
    }
  }

  // Delete patient
  async deletePatient(patientId) {
    await this.initialize();
    
    if (this.apiAvailable) {
      try {
        return await deletePatientAPI(patientId);
      } catch (error) {
        console.warn('API failed, falling back to mock mode');
        this.apiAvailable = false;
        return this.deletePatientMock(patientId);
      }
    } else {
      return this.deletePatientMock(patientId);
    }
  }

  // Mock operations for fallback
  createPatientMock(patientData) {
    const newPatient = {
      ...patientData,
      id: Date.now(),
      nameKey: 'default', // Use default translation key for new patients
    };
    this.mockData.push(newPatient);
    return newPatient;
  }

  updatePatientMock(patientId, patientData) {
    const index = this.mockData.findIndex(p => p.id === patientId);
    if (index !== -1) {
      this.mockData[index] = { ...this.mockData[index], ...patientData };
      return this.mockData[index];
    }
    throw new Error('Patient not found');
  }

  deletePatientMock(patientId) {
    const index = this.mockData.findIndex(p => p.id === patientId);
    if (index !== -1) {
      this.mockData.splice(index, 1);
      return true;
    }
    throw new Error('Patient not found');
  }

  // Check if using real API
  isUsingAPI() {
    return this.apiAvailable === true;
  }

  // Get data source info
  getDataSourceInfo() {
    return {
      isAPI: this.apiAvailable === true,
      source: this.apiAvailable ? 'Real Database' : 'Mock Data',
      patientCount: this.mockData.length
    };
  }
}

// Export singleton instance
export const patientService = new PatientService();

// Export individual functions for direct use
export {
  checkAPIAvailability,
  fetchPatientsFromAPI,
  createPatientAPI,
  updatePatientAPI,
  deletePatientAPI,
  getMockPatients
};
