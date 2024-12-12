import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProfilePage = () => {
    // State management hooks
  // history: stores user's emission query history
  // error: manages any error messages during data fetching
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
      // useEffect hook to fetch user's query history when component mounts
    // Async function to fetch history from backend
    const fetchHistory = async () => {
      try {
        // Log the authentication token (for debugging)
        console.log(localStorage.getItem('authToken'));
        // Retrieve authentication token from local storage
        const token = localStorage.getItem('authToken');
        // Send GET request to profile endpoint with authorization
        const response = await axios.get('http://127.0.0.1:4444/profile', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        // Update history state with fetched data
        setHistory(response.data);
      } catch (err) {
        // Set error message if history fetch fails
        setError('Failed to fetch history. Please try again.');
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="profile-page">
      <h1 className="page-title">User Query History</h1>
      {error && <p className="error">{error}</p>}
      <div className="table-container">
        {history.length > 0 ? (
          <table className="table">
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
                  <td>
                    {Array.isArray(record.recommendations) ? (
                      record.recommendations.map((rec, recIndex) => (
                        <p key={recIndex}>{rec}</p>
                      ))
                    ) : (
                      record.recommendations || 'None'
                    )}
                  </td>
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
