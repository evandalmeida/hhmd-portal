import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClinicDashboard from './Clinic/ClinicDash';
import PatientDashboard from './Patient/PatientDash';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [userRole, setUserRole] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:5555/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.status === 200) {
        const userData = await response.json();
        setUserRole(userData.role);

        if (userData.role === 'clinic_admin') {
          navigate('/clinic-dashboard');
        } else if (userData.role === 'patient') {
          navigate('/patient-dashboard');
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
