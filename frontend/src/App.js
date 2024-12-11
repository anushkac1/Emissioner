import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginPage from './components/login';
import Register from './components/Register'; // Import the Register component
import EmissionChecker from './components/EmissionChecker';
import CommunityPage from './components/CommunityPage';
import ProfilePage from './components/profilePage';
import Navbar from './components/Navbar';
import './App.css';

const App = () => {
  const isAuthenticated = !!localStorage.getItem('authToken'); // Check if user is logged in

  // Custom component to wrap the app logic
  const AppContent = () => {
    const location = useLocation();
    const noNavbarRoutes = ['/login', '/register', '/logout']; // Routes where Navbar is hidden

    return (
      <>
        {/* Display Navbar only when user is authenticated and not on specified routes */}
        {isAuthenticated && !noNavbarRoutes.includes(location.pathname) && <Navbar />}
        <Routes>
          {/* Login Route */}
          <Route path="/login" element={<LoginPage />} />

          {/* Register Route */}
          <Route path="/register" element={<Register />} />

          {/* Default Route */}
          <Route
            path="/"
            element={isAuthenticated ? <Navigate to="/emission-checker" /> : <Navigate to="/login" />}
          />

          {/* Emission Checker (Protected) */}
          <Route
            path="/emission-checker"
            element={isAuthenticated ? <EmissionChecker /> : <Navigate to="/login" />}
          />

          {/* Community Page (Protected) */}
          <Route
            path="/community"
            element={isAuthenticated ? <CommunityPage /> : <Navigate to="/login" />}
          />

          {/* Profile Page (Protected) */}
          <Route
            path="/profile"
            element={isAuthenticated ? <ProfilePage /> : <Navigate to="/login" />}
          />
        </Routes>
      </>
    );
  };

  return (
    <Router>
      <div className="App">
        <AppContent />
      </div>
    </Router>
  );
};

export default App;
