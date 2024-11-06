import React, { useState } from 'react';
import axios from 'axios';

const EmissionChecker = () => {
  const [food, setFood] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (event) => {
    setFood(event.target.value);
  };

  const checkEmissions = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/get_emission', { food });
      setResult(response.data);
      setError(null);
    } catch (err) {
      setError('Could not retrieve data. Please try again.');
      setResult(null);
    }
  };

  return (
    <div className="emission-checker">
      <h1>Emissioner</h1>
      <input
        type="text"
        value={food}
        onChange={handleInputChange}
        placeholder="Enter food item"
      />
      <button onClick={checkEmissions}>Check Emissions</button>

      {error && <p className="error">{error}</p>}
      {result && (
        <div className="result">
          <p>Carbon Emission for {result.food}: {result.carbon_emission} kg CO₂</p>
          <p>Recommendations:</p>
          <ul>
            {result.recommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default EmissionChecker;
