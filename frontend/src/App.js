// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// import LoginPage from './components/login';
// import EmissionChecker from './components/EmissionChecker';
// import CommunityPage from './components/CommunityPage';
// // import ProfilePage from './components/ProfilePage'; // New ProfilePage component
// import ProfilePage from './components/profilePage';
// import Navbar from './components/Navbar'; // Import the Navbar component
// import './App.css';

// const App = () => {
//   const isAuthenticated = !!localStorage.getItem('authToken'); // Check if user is logged in

//   return (
//     <Router>
//       <div className="App">
//         {isAuthenticated && <Navbar />} {/* Display Navbar only when user is authenticated */}
//         <Routes>
//           <Route path="/login" element={<LoginPage />} />
          
//           {/* Default route checks authentication */}
//           <Route 
//             path="/" 
//             element={isAuthenticated ? <Navigate to="/emission-checker" /> : <Navigate to="/login" />}
//           />
          
//           {/* Emission checker page is protected */}
//           <Route 
//             path="/emission-checker" 
//             element={isAuthenticated ? (
//               <EmissionChecker />
//             ) : (
//               <Navigate to="/login" />
//             )}
//           />
          
//           {/* Community Page is protected */}
//           <Route 
//             path="/community" 
//             element={isAuthenticated ? (
//               <CommunityPage />
//             ) : (
//               <Navigate to="/login" />
//             )}
//           />
          
//           {/* Profile Page is protected */}
//           <Route 
//             path="/profile" 
//             element={isAuthenticated ? (
//               <ProfilePage />
//             ) : (
//               <Navigate to="/login" />
//             )}
//           />
//         </Routes>
//       </div>
//     </Router>
//   );
// };

// export default App;






import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/login';
import Register from './components/Register'; // Import the Register component
import EmissionChecker from './components/EmissionChecker';
import CommunityPage from './components/CommunityPage';
import ProfilePage from './components/profilePage';
import Navbar from './components/Navbar';
import './App.css';

const App = () => {
  const isAuthenticated = !!localStorage.getItem('authToken'); // Check if user is logged in

  return (
    <Router>
      <div className="App">
        {isAuthenticated && <Navbar />} {/* Display Navbar only when user is authenticated */}
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
      </div>
    </Router>
  );
};

export default App;
