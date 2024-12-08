import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate(); // Hook for navigation

  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
    console.log(email);
    console.log(password);
      const response = await axios.post('http://127.0.0.1:4444/login', { email, password });
      console.log(response);
      
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token); // Store JWT token
        console.log("navigating");
        navigate('/emission-checker'); // Redirect to EmissionChecker
      }

    } catch (err) {
      setError('incorrect credentials');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <p>{error}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
