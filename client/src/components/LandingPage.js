import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const LandingPage = ({ setCurrentUser, currentUser, logout }) => {
  const navigate = useNavigate();

  const selectRole = (role) => {
    if (currentUser && currentUser.role !== role) {
      setCurrentUser({ role });
    }
    navigate(`/${role}-registration`);
  };

  const handleLogin = () => {
    navigate('/');
  };



  return (
    <div>
      <h1 className='heading'>WELCOME!</h1>
      {currentUser ? (
        <div>
          <p>You are logged in as {currentUser.user?.role}</p>
          {currentUser.user?.role === 'clinic_admin' && (
            <Link to="/clinic-dashboard">Clinic Dashboard Link</Link>
          )}
          {currentUser.user?.role === 'patient' && (
            <Link to="/patient-dashboard">Patient Dashboard Link</Link>
          )}
          <button onClick={handleLogin}>logout</button>
        </div>
      ) : (
        <div className='buttons'>
          <button className='homebutton' onClick={() => selectRole('clinic_admin')}>
            Register as Clinic
          </button>
          <button className='homebutton' onClick={() => selectRole('patient')}>
            Register as Patient
          </button>
          <button className='homebutton' onClick={handleLogin}>
            Login
          </button>
        </div>
      )}
    </div>
  );
};

export default LandingPage;