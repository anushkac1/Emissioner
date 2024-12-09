import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/login';
import EmissionChecker from './components/EmissionChecker';
import CommunityPage from './components/CommunityPage';  // Import the CommunityPage component
import './App.css';

const App = () => {
  const isAuthenticated = !!localStorage.getItem('authToken'); // Check if user is logged in

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        {/* Default route checks authentication */}
        <Route 
          path="/" 
          element={isAuthenticated ? <Navigate to="/emission-checker" /> : <Navigate to="/login" />}
        />
        
        {/* Emission checker page is protected */}
        <Route 
          path="/emission-checker" 
          element={isAuthenticated ? (
            <div className="App">
              <EmissionChecker />
            </div>
          ) : (
            <Navigate to="/login" />
          )}
        />
        
        {/* Community Page is protected */}
        <Route 
          path="/community" 
          element={isAuthenticated ? (
            <div className="App">
              <CommunityPage />
            </div>
          ) : (
            <Navigate to="/login" />
          )}
        />
      </Routes>
    </Router>
  );
};

export default App;
