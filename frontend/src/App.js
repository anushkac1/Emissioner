// import React from 'react';
// import EmissionChecker from './components/EmissionChecker';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <EmissionChecker />
//     </div>
//   );
// }

// export default App;

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/login';
import EmissionChecker from './components/EmissionChecker'; 
import './App.css';
const App = () => {
  const isAuthenticated = !!localStorage.getItem('authToken'); // Check if user is logged in

  return (
    <Router>
      <Routes>
        <Route path="/login" element={ <LoginPage />} />
        <Route path="/" element={isAuthenticated ? <Navigate to="/emission-checker" /> : <LoginPage />} />
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
      </Routes>
    </Router>
  );
};

export default App;
