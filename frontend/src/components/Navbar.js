import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();  // For redirecting after logout

  const handleLogout = () => {
    // Clear auth token or authentication state
    localStorage.removeItem('authToken');
    navigate('/login');  // Redirect to login page after logout
  };

  return (
    <nav style={navbarStyles}>
      <ul style={ulStyles}>
        <li style={liStyles}>
          <Link to="/emission-checker" style={linkStyles}>Emission Checker</Link>
        </li>
        <li style={liStyles}>
          <Link to="/profile" style={linkStyles}>Profile</Link>
        </li>
        <li style={liStyles}>
          <Link to="/community" style={linkStyles}>Community</Link>
        </li>
        <li style={liStyles}>
          <button onClick={handleLogout} style={logoutButtonStyles}>Logout</button>
        </li>
      </ul>
    </nav>
  );
};

// Styles for navbar
const navbarStyles = {
  backgroundColor: '#333',
  padding: '3px',
};

const ulStyles = {
  listStyleType: 'none',
  padding: '0',
  margin: '0',
  display: 'flex',
  justifyContent: 'space-around',
};

const liStyles = {
  margin: '0 10px',
};

const linkStyles = {
  textDecoration: 'none',
  color: 'white',
  fontSize: '16px',
};

const logoutButtonStyles = {
  backgroundColor: '#f44336',
  color: 'white',
  border: 'none',
  padding: '10px 15px',
  fontSize: '16px',
  cursor: 'pointer',
};

export default Navbar;

