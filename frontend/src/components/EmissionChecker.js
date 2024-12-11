// import React, { useState } from 'react';
// import axios from 'axios';

// const EmissionChecker = () => {
//   const [food, setFood] = useState('');
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState(null);

//   const handleInputChange = (event) => {
//     setFood(event.target.value);
//   };

//   const checkEmissions = async () => {
//     try {
//       // const response = await axios.post('http://127.0.0.1:4444/get_emission', { food });
//       const response = await axios.post('http://127.0.0.1:4444/get_emission', { food });
//       setResult(response.data);
//       setError(null);
//     } catch (err) {
//       setError('Could not retrieve data. Please try again.');
//       setResult(null);
//     }
//   };

//   return (
//     <div className="emission-checker">
//       <h1>Emissioner</h1>
//       <input
//         type="text"
//         value={food}
//         onChange={handleInputChange}
//         placeholder="Enter food item"
//       />
//       <button onClick={checkEmissions}>Check Emissions</button>

//       {error && <p className="error">{error}</p>}
//       {result && result.error && <p className="error">{result.error}</p>}
//       {result && result.emission && (
//         <div className="result">
//           <p>Carbon Emission for {result.food}: {result.emission} kg CO₂</p>
//         </div>
//       )}
//     </div>
//   );
// };

// export default EmissionChecker;


import React, { useState } from 'react';
import axios from 'axios';
// import '../App.css';

const EmissionChecker = () => {
  const token = localStorage.getItem("authToken");
  console.log("The token when the emission page first loads: ", token);
  const [food, setFood] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => setFood(e.target.value);

  const checkEmissions = async () => {
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
    }
  };
  
  return (
    // <div className="emission-checker">
    //   <h1>Emissioner</h1>
    //   <input type="text" value={food} onChange={handleInputChange} placeholder="Enter food item" />
    //   <button onClick={checkEmissions}>Check Emissions</button>

    //   {error && <p className="error">{error}</p>}
    //   {result && result.error && <p className="error">{result.error}</p>}
    //   {result && (
    //     <div className="result">
    //       <p><strong>Carbon Emission for {result.food}:</strong> {result.emission} kg CO₂</p>
    //       {result.recommendations && (
    //         <>
    //           <h3>Eco-friendly Alternatives:</h3>
    //           <pre>{result.recommendations}</pre>
    //         </>
    //       )}
    //     </div>
    //   )}
    // </div>
    <div className="emission-checker">
    <h1>Emissioner</h1>
    <input type="text" value={food} onChange={handleInputChange} placeholder="Enter food item" />
    <button onClick={checkEmissions}>Check Emissions</button>

    {result && (
      <div className="result">
        <p><strong>Carbon Emission for {result.food}:</strong> {result.emission}</p>
        {result.recommendations && (
          <div className="alternatives-section">
            <h3>Eco-friendly Alternatives:</h3>
            <div className="alternatives-text">
              {result.recommendations.split("\n").map((item, index) => (
                <p key={index}>{item}</p>
              ))}
            </div>
          </div>
        )}
      </div>
    )}
  </div>

  );
};

export default EmissionChecker;