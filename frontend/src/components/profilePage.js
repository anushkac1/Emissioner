// import React from 'react';

// const ProfilePage = () => {
//   return (
//     <div>
//       <h1>Your Profile</h1>
//       <p>Welcome to your profile page!</p>
//       {/* Add your profile details here */}
//     </div>
//   );
// };

// export default ProfilePage;


import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProfilePage = () => {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        console.log(localStorage.getItem('authToken'));

        const token = localStorage.getItem('authToken');
        const response = await axios.get('http://127.0.0.1:4444/profile', {
            headers: { 'Authorization': `Bearer ${token}` ,
            'Content-Type': 'application/json'},
            
        });
        setHistory(response.data);
      } catch (err) {
        setError('Failed to fetch history. Please try again.');
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="profile-page">
      <h1>User Query History</h1>
      {error && <p className="error">{error}</p>}
      <div className="history-container">
        {history.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Food Item</th>
                <th>Emission (kg CO₂)</th>
                <th>Recommendations</th>
              </tr>
            </thead>
            <tbody>
              {history.map((record, index) => (
                <tr key={index}>
                  <td>{record.food_item}</td>
                  <td>{record.emission}</td>
                  <td>{record.recommendations || 'None'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No query history found.</p>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;