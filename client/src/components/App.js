
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import ClinicRegistration from './Main/UserPanel/Clinic/ClinicRegistration'; 
import PatientRegistration from './Main/UserPanel/Patient/PatientRegistration';
import Login from './Main/UserPanel/Login';
import ClinicDashboard from './Main/UserPanel/Clinic/ClinicDash';
import PatientDashboard from './Main/UserPanel/Patient/PatientDash';
import LandingPage from './LandingPage';


const App = () => {
  const [currentUser, setCurrentUser] = useState({});


  async function attemptClinicSignup(userInfo) {
    const res = await fetch('/clinic_admin-registration', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentUser.access_token}`
      },
      body: JSON.stringify(userInfo)
    });
    if (res.ok) {
      const data = await res.json();
      setCurrentUser(data);
    } else {
      const errorData = await res.json();
      alert(errorData.error || 'Invalid sign up');
    }
  }

  async function attemptLogin(userInfo) {
    const res = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userInfo)
    });
    if (res.ok) {
      const data = await res.json();
      setCurrentUser(data);
      return data;
    } else {
      alert('Invalid login');
      return false;
    }
  }

  function logout() {
    setCurrentUser(null);
    fetch('/logout', {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${currentUser.access_token}`
      },
    });
  }

  
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<LandingPage currentUser={currentUser} logout={logout}/>} />
          <Route path="/clinic_admin-registration" element={<ClinicRegistration attemptLogin={attemptLogin} setCurrentUser={setCurrentUser} attemptClinicSignup={attemptClinicSignup}/>} />
          <Route path="/patient-registration" element={<PatientRegistration setCurrentUser={setCurrentUser} />} />
          <Route path="/login" element={<Login attemptLogin={attemptLogin} />} />
          <Route
            path={
              currentUser && currentUser.user?.role === 'clinic_admin'
                ? '/clinic-dashboard'
                : currentUser && currentUser.user?.role === 'patient'
                ? '/patient-dashboard'
                : null
            }
            element={
              currentUser && currentUser.user?.role === 'clinic_admin'
                ? <ClinicDashboard currentUser={currentUser} logout={logout} />
                : currentUser && currentUser.user?.role === 'patient'
                ? <PatientDashboard currentUser={currentUser} logout={logout} />
                : null 
            }
          />
        </Routes>
      </div>
    </Router>
  );
};


export default App;


