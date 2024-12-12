import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import logo2 from './assets/logoCrop.png'; //import the logo


const LoginPage = () => {
  // Retrieve existing authentication token from local storage
    const token = localStorage.getItem("authToken");
  console.log("The token when the login page first loads: ", token);
   // State management hooks
  // email: stores user's email input
  // password: stores user's password input
  // error: manages login error messages
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
    // Navigation hook for programmatic routing
  const navigate = useNavigate();
  // Async function to handle user login
  const handleLogin = async (e) => {
    // Prevent default form submission behavior
    e.preventDefault();
    try {
      // Send POST request to login endpoint
        console.log("login in is being it");
      const response = await axios.post('http://127.0.0.1:4444/login', { email, password });
       // Check if token is received in response
      if (response.data.token) {
        // Store authentication token in local storage
        localStorage.setItem('authToken', response.data.token);
        console.log("The current user's token that was just set by login:", localStorage.getItem("authToken"));
        // Navigate to emission checker page after successful login
        navigate('/emission-checker');
      }
    } catch (err) {
      // Set error message if login fails
      setError('Incorrect credentials');
    }
  };

  return (
    <div className="container">
      {/* Image in the center */}
      <div className="image-container">
        <img src={logo2} alt="Eco-friendly illustration" className="logo-normal"/>
      </div>
      <div className="form_area">
        <h2 className="title">Login</h2>
        {error && <p className="sub_title">{error}</p>}
        <form onSubmit={handleLogin}>
          <div className="form_group">
            <label htmlFor="email" className="sub_title">Email:</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form_style"
              required
            />
          </div>
          <div className="form_group">
            <label htmlFor="password" className="sub_title">Password:</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form_style"
              required
            />
          </div>
          <button type="submit" className="btn">Login</button>
        </form>
        
        {/* Add this button for navigating to the registration page */}
        <button 
          onClick={() => navigate('/register')} 
          className="btn"
          style={{ background: '#9fc7aa', marginTop: '10px' }}
        >
          Register
        </button>
      </div>
    </div>
  );
};

export default LoginPage;

