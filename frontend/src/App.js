import React, { useState } from 'react';
import './App.css';

function App() {
  const [foodItem, setFoodItem] = useState('');
  const [emissionData, setEmissionData] = useState(null);
  const [error, setError] = useState(null);

  const handleFoodChange = (e) => {
    setFoodItem(e.target.value);
  };

  const fetchEmissionData = async () => {
    setError(null); // Reset any previous errors
    try {
      const response = await fetch('http://localhost:4444/get_emission', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ food: foodItem }),
      });

      const data = await response.json();

      if (data.error) {
        setError(data.error);
        setEmissionData(null);
      } else {
        setEmissionData(data);
      }
    } catch (err) {
      setError("An error occurred while fetching data.");
      setEmissionData(null);
    }
  };

  return (
    <div className="App">
      <div className="emission-checker">
        <div className="title">Carbon Emission for Food</div>

        {/* Display food emission result */}
        {emissionData && (
          <div className="food-emission">
            {emissionData.emission} kg CO2 per kilogram of {emissionData.food}
          </div>
        )}

        {/* Display error message */}
        {error && <div className="error">{error}</div>}

        <input
          type="text"
          value={foodItem}
          onChange={handleFoodChange}
          placeholder="Enter a food item (e.g., eggs)"
        />

        {/* Custom styled button */}
        <button className="pushable" onClick={fetchEmissionData}>
          <span className="shadow"></span>
          <span className="edge"></span>
          <span className="front">Get Emission</span>
        </button>
      </div>
    </div>
  );
}

export default App;