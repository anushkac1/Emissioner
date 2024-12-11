import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import logo from './assets/logo.png';  // Import the logo image

const Navbar = () => {
  const navigate = useNavigate();  // For redirecting after logout

  const handleLogout = () => {
    // Clear auth token or authentication state
    localStorage.removeItem('authToken');
    navigate('/login');  // Redirect to login page after logout
  };

  return (
    <nav style={navbarStyles}>
      <div style={logoContainerStyles}>
        <img src={logo} alt="Logo" style={logoStyles} />
      </div>
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
  backgroundColor: '#06402B',
  padding: '10px 5px', // Adjust padding to create space
  display: 'flex',
  justifyContent: 'space-between', // Align logo to the left and nav items to the right
  alignItems: 'center', // Center vertically
};

const logoContainerStyles = {
  display: 'flex',
  alignItems: 'center',
};

const logoStyles = {
  width: '200px',  // Adjust the width of the logo
  height: 'auto',
};

const ulStyles = {
    
  listStyleType: 'none',
  padding: '0',
  margin: '0',
  display: 'flex',
  justifyContent: 'flex-end', // Aligns items to the right
  gap: '50px', // Adds spacing between items
};

const liStyles = {
    margin: '0 10px',
    marginTop: '10px',  // Adds space to the top of each list item, moving them down
  };
  
const linkStyles = {
  textDecoration: 'none',
  color: 'white',
  fontSize: '16px',
};

const logoutButtonStyles = {
    marginTop: '-3px',
    backgroundColor: '#9fc7aa',
    color: '#06402B',
    border: 'none',
    padding: '5px 20px',
    fontSize: '16px',
    cursor: 'pointer',
    marginLeft: '-5px', // Moves the whole button 10px to the left
    fontWeight: 'bold',  // Make the text inside the button bold
  };
  

export default Navbar;

