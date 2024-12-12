/*
  Please Note: We utilized Canva for creating our logo and https://uiverse.io/barisdogansutcu/light-rat-32 (uiverse) to 
  include nicer graphics in our frontend!

  This is the app.js file that overall just deals with the core structure of our app, primarily pertaining to the 
  frontend side of things. This is where we deal with some of the routing, authentication, and basic conditions 
  on the overall app!
*/



//basic import statements needed for this file 
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginPage from './components/login';
import Register from './components/Register'; // Import the Register component
import EmissionChecker from './components/EmissionChecker';
import CommunityPage from './components/CommunityPage';
import ProfilePage from './components/profilePage';
import Navbar from './components/Navbar';
import './App.css';



//main app component 
const App = () => {
  //if authenticated - deal with token to see if user is logged in 
  const isAuthenticated = !!localStorage.getItem('authToken'); 

  //additional component to handle inner page routing 
  const AppContent = () => {
    //where is the user currently? on what page?
    const location = useLocation();
    //configure where the user cannot see the navbar
    const noNavbarRoutes = ['/login', '/register', '/logout']; 

    return (
      <>
        {/* Navbar only when user logged in - avoid on login and registration pages */}
        {isAuthenticated && !noNavbarRoutes.includes(location.pathname) && <Navbar />}
        <Routes>
          {/* login in route - no navbar*/}
          <Route path="/login" element={<LoginPage />} />

          {/* registration route - no navbar*/}
          <Route path="/register" element={<Register />} />

          {/* once autneticated, show navbar - enter emission-checker page */}
          <Route
            path="/"
            element={isAuthenticated ? <Navigate to="/emission-checker" /> : <Navigate to="/login" />}
          />

          {/* emission checker page - only if user logged in */}
          <Route
            path="/emission-checker"
            element={isAuthenticated ? <EmissionChecker /> : <Navigate to="/login" />}
          />

          {/* community page */}
          <Route
            path="/community"
            element={isAuthenticated ? <CommunityPage /> : <Navigate to="/login" />}
          />

          {/* profile page specific to user logged in  */}
          <Route
            path="/profile-page"
            element={isAuthenticated ? <ProfilePage /> : <Navigate to="/login" />}
          />
        </Routes>
      </>
    );
  };

  //return component 
  return (
    <Router>
      <div className="App">
        <AppContent />
      </div>
    </Router>
  );
};

//export app 
export default App;
