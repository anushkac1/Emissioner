import React, { useState } from 'react';
import axios from 'axios';
import logo2 from './assets/logoCrop.png'; // Adjust the extension to match your file

const EmissionChecker = () => {
  const token = localStorage.getItem("authToken");
  console.log("The token when the emission page first loads: ", token);
  const [food, setFood] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false); // Added loading state

  const handleInputChange = (e) => setFood(e.target.value);

  const checkEmissions = async () => {
    setLoading(true); // Start loading
    const token = localStorage.getItem("authToken"); // Retrieve the token from localStorage
    // console.log("checkEmissions method is hit and this is the user token:", token);
    // console.log("This is the food they are trying to input:", {food});
    try {
      const response = await axios.post(
        "http://127.0.0.1:4444/get-emission",
        {food},
        {
          headers: {
            Authorization: `Bearer ${token}`, // Attach the token in the Authorization header
            "Content-Type": "application/json", // Explicitly set JSON content type
          },
        }
      );
      // console.log(response.get_json());
      setResult(response.data);
      setError(null);
    } catch (err) {
      // console.log(err);
      if (err.response?.status === 401) {
        setError("Unauthorized. Please log in again.");
      } else {
        setError("Could not retrieve data. Please try again.");
      }
      setResult(null);
    } finally {
      setLoading(false); // Stop loading
    }
  };
  
  return (
    <div className="emission-checker">
      {/* Image in the center */}
      <div className="image-container">
        <img src={logo2} alt="Eco-friendly illustration" className="logo-large"/>
      </div>

      {/* Centered content */}
      <div className="content-container">
        <p className="instruction">
          Enter a food item below to discover its carbon emissions and eco-friendly alternatives.
        </p>
        <input
          type="text"
          value={food}
          onChange={handleInputChange}
          placeholder="Enter food item"
          className="input-box"
        />
        <button onClick={checkEmissions} className="submit-button">
          Check Emissions
        </button>
      </div>

      {/* Loader */}
      {loading && (
        <div className="loader">
          <svg viewBox="25 25 50 50">
            <circle r="20" cy="50" cx="50"></circle>
          </svg>
        </div>
      )}

      {/* Results */}
      {!loading && result && (
        <div className="result">
          <p>
            <strong>Carbon Emission for {result.food}:</strong> {result.emission}
          </p>
          {result.recommendations && (
            <div className="alternatives-section">
              <h3>Eco-friendly Alternatives:</h3>
              <div className="alternatives-text">
                {result.recommendations.split('\n').map((item, index) => (
                  <p key={index}>{item}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error */}
      {!loading && error && <p className="error">{error}</p>}
    </div>
  );
};

export default EmissionChecker;
