

import React, { useState } from 'react';
import { useNavigate, useOutletContext } from 'react-router-dom';
import ClinicDashboard from './Clinic/ClinicDash';
import PatientDashboard from './Patient/PatientDash';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [userRole, setUserRole] = useState(null);

  const navigate = useNavigate();
  const {attemptLogin} = useOutletContext() ?? {} ;

  async function handleLogin(e) {
    e.preventDefault();
  
    try {
      const loginInfo = {
        email: email,
        password: password,
      };
  
      const response = await attemptLogin(loginInfo);
  
      if (response) {
        setUserRole(response?.role);
  
        if (response?.role === 'clinic_admin') {
          navigate('/clinic-dashboard');
        } else if (response?.role === 'patient') {
          navigate('/patient-dashboard');
        } else {
          setError('Invalid email or password');
        }
      } else {
        setError('Invalid email or password');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('An error occurred during login');
    }
  }
  
  

  return (
    <form className='form'>
      <h2 className='heading'>LOGIN</h2>
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