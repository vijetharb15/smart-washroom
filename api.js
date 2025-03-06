import axios from "axios";

const API_URL = "http://130.1.99.27:5000/sensor-data";

export const fetchSensorData = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    console.error("Error fetching sensor data:", error);
    return {
      odorLevel: 0,
      soapLevel: 0,
      motionDetected: false
    };
  }
};