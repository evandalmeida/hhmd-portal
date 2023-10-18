

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClinicDashboard from './Clinic/ClinicDash';
import PatientDashboard from './Patient/PatientDash';

const Login = ({ attemptLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [userRole, setUserRole] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const loginInfo = {
        email: email,
        password: password,
      };
  
      const loginSuccess = await attemptLogin(loginInfo);
      
      if (loginSuccess) {
        setUserRole(loginSuccess.user.role);
  
        if (loginSuccess.user.role === 'clinic_admin') {
          navigate('/clinic-dashboard');  // No need for full URL
        } else if (loginSuccess.user.role === 'patient') {
          navigate('/patient-dashboard');  // No need for full URL
        }
      } else {
        setError('Invalid email or password');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('An error occurred during login');
    }
  };
  

  return (
    <form className='form'>
      <h2 className='heading'>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        autoComplete="current-password" 
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {error && <p>{error}</p>}
      <button onClick={handleLogin}>Login</button>

      {userRole === 'clinic_admin' && <ClinicDashboard />}
      {userRole === 'patient' && <PatientDashboard />}
    </form>
  );
};

export default Login;
