import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import logo from './assets/logo.png';  //import logo

const Navbar = () => {
      // Navigation hook for programmatic routing
  const navigate = useNavigate(); 
  // Logout handler function
  const handleLogout = () => {
    // Remove authentication token from local storage
    // This effectively logs out the user
    localStorage.removeItem('authToken');
    // Redirect to login page after logout
    navigate('/login');  
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
          <Link to="/profile-page" style={linkStyles}>Profile</Link>
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


const navbarStyles = {
  backgroundColor: '#06402B',
  padding: '10px 5px', 
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center', 
};

const logoContainerStyles = {
  display: 'flex',
  alignItems: 'center',
};

const logoStyles = {
  width: '200px',  
  height: 'auto',
};

const ulStyles = {
    
  listStyleType: 'none',
  padding: '0',
  margin: '0',
  display: 'flex',
  justifyContent: 'flex-end',
  gap: '50px', 
};

const liStyles = {
    margin: '0 10px',
    marginTop: '10px',  
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
    marginLeft: '-5px', 
    fontWeight: 'bold',  
  };
  

export default Navbar;

