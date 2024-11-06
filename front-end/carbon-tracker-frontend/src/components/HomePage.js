import React, { useState } from 'react';
import Navbar from './Navbar';  // Import Navbar component

function HomePage() {
  const [food, setFood] = useState('');
  const [emissions, setEmissions] = useState(null);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    setEmissions({
      amount: 4.5,
      alternatives: ["Tofu", "Chickpea Flour", "Just Egg"],
    });
  };

  return (
    <div className="min-h-screen bg-green-900 flex flex-col items-center justify-center text-white px-4">
      <h1 className="text-3xl font-light mb-8">Emissioner</h1>

      {/* Emissions Meter Placeholder */}
      <div className="flex flex-col items-center mb-6">
        <div className="w-32 h-32 bg-gray-800 rounded-full flex items-center justify-center">
          <span className="text-4xl">{emissions ? emissions.amount : "--"}</span>
        </div>
        <span className="text-xl mt-2">{emissions ? "Kg CO2" : "Kg CO2"}</span>
      </div>

      {/* Emissions Details Placeholder */}
      {emissions && (
        <p className="text-center mb-4 text-sm">
          Eggs have a total carbon footprint of {emissions.amount} Kg CO2 - equivalents per kg product
          <br />
          Alternatives: {emissions.alternatives.map((alt, index) => (
            <span key={index} className="text-teal-300">
              {index > 0 && ", "}
              {alt}
            </span>
          ))}
        </p>
      )}

      {/* Food Input Form */}
      <form onSubmit={handleFormSubmit} className="w-full max-w-xs">
        <input
          type="text"
          value={food}
          onChange={(e) => setFood(e.target.value)}
          placeholder="Enter food item"
          className="w-full px-4 py-2 border border-gray-300 rounded-md text-black mb-4"
        />
        <button
          type="submit"
          className="w-full bg-teal-700 py-2 rounded-md hover:bg-teal-800"
        >
          Submit
        </button>
      </form>

      {/* Include Navbar */}
      <Navbar />
    </div>
  );
}

export default HomePage;
