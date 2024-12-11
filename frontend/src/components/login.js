
// import React, { useState } from 'react';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom';

// const LoginPage = () => {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');
//   const navigate = useNavigate();

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await axios.post('http://127.0.0.1:4444/login', { email, password });
//       if (response.data.token) {
//         localStorage.setItem('authToken', response.data.token);
//         navigate('/emission-checker');
//       }
//     } catch (err) {
//       setError('Incorrect credentials');
//     }
//   };

//   return (
//     <div className="container">
//       <div className="form_area">
//         <h2 className="title">Login</h2>
//         {error && <p className="sub_title">{error}</p>}
//         <form onSubmit={handleLogin}>
//           <div className="form_group">
//             <label htmlFor="email" className="sub_title">Email:</label>
//             <input
//               id="email"
//               type="email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               className="form_style"
//               required
//             />
//           </div>
//           <div className="form_group">
//             <label htmlFor="password" className="sub_title">Password:</label>
//             <input
//               id="password"
//               type="password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               className="form_style"
//               required
//             />
//           </div>
//           <button type="submit" className="btn">Login</button>
//         </form>
//       </div>
//     </div>
//   );
// };

// export default LoginPage;



import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const token = localStorage.getItem("authToken");
  console.log("The token when the login page first loads: ", token);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
        console.log("login in is being it");
      const response = await axios.post('http://127.0.0.1:4444/login', { email, password });
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token);
        console.log("The current user's token that was just set by login:", localStorage.getItem("authToken"));
        navigate('/emission-checker');
      }
    } catch (err) {
      setError('Incorrect credentials');
    }
  };

  return (
    <div className="container">
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
          style={{ background: '#007bff', marginTop: '10px' }}
        >
          Register
        </button>
      </div>
    </div>
  );
};

export default LoginPage;

