import axios from 'axios';

// The base URL will be proxied to the FastAPI backend thanks to the "proxy" setting in package.json
const API_URL = '/api/simulate';

/**
 * Calls the simulation API with the provided input data.
 * @param {object} inputData - The data for the simulation, matching either DesignerModeInput or PlantModeInput.
 * @returns {Promise<object>} - A promise that resolves to the simulation result data.
 */
export const runSimulation = async (inputData) => {
  try {
    const response = await axios.post(API_URL, inputData);
    return response.data;
  } catch (error) {
    // Handle different kinds of errors
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error("API Error:", error.response.data);
      // Re-throw a more user-friendly error message
      throw new Error(error.response.data.detail || 'An error occurred on the server.');
    } else if (error.request) {
      // The request was made but no response was received
      console.error("Network Error:", error.request);
      throw new Error('Network error: Could not connect to the server. Is the backend running?');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error("Error:", error.message);
      throw new Error('An unexpected error occurred.');
    }
  }
};