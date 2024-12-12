import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo2 from './assets/logoCrop.png'; //import logo


const Register = () => {
   // State hooks to manage form inputs and messages
  // email: stores the user's email input
  // password: stores the user's password input
  // message: displays registration status or error messages
   // navigate: allows programmatic navigation between routes
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); 
// Async function to handle user registration
  const handleRegister = async (e) => {
        // Prevent the default form submission behavior
    e.preventDefault();

    try {
      // Send a POST request to the registration endpoint
      const response = await fetch('http://localhost:4444/register', {
        method: 'POST',
        // Set the content type to JSON
        headers: {
          'Content-Type': 'application/json',
        },
        // Convert email and password to JSON string for the request body
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      // Check if the registration was successful
      if (response.ok) {
        setMessage('User registered successfully!');
      } else {
        setMessage(data.message || 'Failed to register user.');
      }
    } catch (error) {
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      {/* Image in the center */}
      <div className="image-container">
        <img src={logo2} alt="Eco-friendly illustration" className="logo-normal"/>
      </div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div>
          <label>Email: </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}

      {/* Button to go back to Login */}
      <button
        onClick={() => navigate('/login')}
        style={{ marginTop: '20px', padding: '10px 20px', background: '#083e13', color: '#fff', border: 'none', cursor: 'pointer', borderRadius: '5px' }}
      >
        Back to Login
      </button>
    </div>
  );
};

export default Register;
