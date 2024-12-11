// import React, { useState } from 'react';
// import axios from 'axios';
// import logo2 from './assets/logoCrop.png'; // Adjust the extension to match your file


// const EmissionChecker = () => {
//   const [food, setFood] = useState('');
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState(null);

//   const handleInputChange = (e) => setFood(e.target.value);

//   const checkEmissions = async () => {
//     try {
//       const response = await axios.post('http://127.0.0.1:4444/get-emission', { food });
//       setResult(response.data);
//       setError(null);
//     } catch (err) {
//       setError('Could not retrieve data. Please try again.');
//       setResult(null);
//     }
//   };

//   return (
//     <div className="emission-checker">
//       {/* Image in the center */}
//       <div className="image-container">
//       <img src={logo2} alt="Eco-friendly illustration" />
//       </div>
//       <input type="text" value={food} onChange={handleInputChange} placeholder="Enter food item" />
//       <button onClick={checkEmissions}>Check Emissions</button>

//       {result && (
//         <div className="result">
//           <p><strong>Carbon Emission for {result.food}:</strong> {result.emission}</p>
//           {result.recommendations && (
//             <div className="alternatives-section">
//               <h3>Eco-friendly Alternatives:</h3>
//               <div className="alternatives-text">
//                 {result.recommendations.split("\n").map((item, index) => (
//                   <p key={index}>{item}</p>
//                 ))}
//               </div>
//             </div>
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default EmissionChecker;
import React, { useState } from 'react';
import axios from 'axios';
import logo2 from './assets/logoCrop.png'; // Adjust the extension to match your file

const EmissionChecker = () => {
  const [food, setFood] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => setFood(e.target.value);

  const checkEmissions = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:4444/get-emission', { food });
      setResult(response.data);
      setError(null);
    } catch (err) {
      setError('Could not retrieve data. Please try again.');
      setResult(null);
    }
  };

  return (
    <div className="emission-checker">
      {/* Image in the center */}
      <div className="image-container">
        <img src={logo2} alt="Eco-friendly illustration" />
      </div>

      {/* Instruction line */}
      <p className="instruction">
        Enter a food item below to discover its carbon emissions and eco-friendly alternatives!
      </p>

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
