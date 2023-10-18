// LandingPage.js

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const LandingPage = ({ setCurrentUser, currentUser }) => {
  const navigate = useNavigate();

  const selectRole = (role) => {
    if (currentUser && currentUser.role !== role) {
      setCurrentUser({ role });
    }

    // Redirect to the registration page for the selected role
    navigate(`/${role}-registration`);
  };

  const handleLogin = () => {
    if (currentUser) {
      if (currentUser.role === 'clinic_admin') {
        navigate('/clinic-dashboard');
      } else if (currentUser.role === 'patient') {
        navigate('/patient-dashboard');
      }
    } else {
      navigate('/login');
    }
  };

  return (
    <div>
      <h1 className='heading'>WELCOME!</h1>

      {currentUser ? (
        <div>
          <p>You are logged in as {currentUser.role}</p>
          {currentUser.role === 'clinic_admin' && (
            <Link to="/clinic-dashboard">Clinic Dashboard Link</Link>
          )}
          {currentUser.role === 'patient' && (
            <Link to="/patient-dashboard">Patient Dashboard Link</Link>
          )}

          <button onClick={handleLogin}>Go to Dashboard</button>
        </div>
      ) : (
        <div className='buttons'>
          <button className='homebutton' onClick={() => selectRole('clinic_admin')}>
            Register as Clinic
          </button>

          <button className='homebutton' onClick={() => selectRole('patient')}>
            Register as Patient
          </button>

          <button className='homebutton' onClick={handleLogin}>Login</button>
        </div>
      )}
    </div>
  );
};

export default LandingPage;
