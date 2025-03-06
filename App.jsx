import React, { useState, useEffect } from "react";
import { fetchSensorData } from "./api";
import { motion } from "framer-motion";
import { FaRestroom } from "react-icons/fa";

export default function App() {
  const [sensorData, setSensorData] = useState({
    odorLevel: 40,
    soapLevel: 75,
    motionDetected: false,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchSensorData();
        setSensorData(data);
      } catch (error) {
        console.error("Failed to update sensor data:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <div className="header">
        <FaRestroom size={32} color="#1a3c34" />
        <h1>Smart Washroom Dashboard</h1>
      </div>
      <div className="grid-container">
        {Object.entries(sensorData).map(([key, value]) => (
          <motion.div
            key={key}
            whileHover={{ scale: 1.03 }}
            className="card"
          >
            <h2>{key.replace(/([A-Z])/g, " $1").trim()}</h2>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${typeof value === "number" ? value : 0}%` }}
              />
            </div>
            <p>
              {key === "motionDetected"
                ? value
                  ? "🚶 Motion Detected"
                  : "✅ No Motion"
                : `${value}%`}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}