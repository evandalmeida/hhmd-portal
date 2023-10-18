import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import ClinicRegistration from './Main/UserPanel/Clinic/ClinicRegistration'; 
import PatientRegistration from './Main/UserPanel/Patient/PatientRegistration';
import Login from './Main/UserPanel/Login';
import ClinicDashboard from './Main/UserPanel/Clinic/ClinicDash';
import PatientDashboard from './Main/UserPanel/Patient/PatientDash';
import LandingPage from './LandingPage';


const App = () => {
  const [currentUser, setCurrentUser] = useState();

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<LandingPage setCurrentUser={setCurrentUser} currentUser={currentUser} />} />
          <Route path="/clinic_admin-registration" element={<ClinicRegistration setCurrentUser={setCurrentUser} />} />
          <Route path="/patient-registration" element={<PatientRegistration setCurrentUser={setCurrentUser} />} />
          <Route path="/login" element={<Login />} />
          {currentUser && currentUser.role === 'clinic_admin' && (
            <Route path="/clinic-dashboard" element={<ClinicDashboard />} />
          )}
          {currentUser && currentUser.role === 'patient' && (
            <Route path="/patient-dashboard" element={<PatientDashboard />} />
          )}
        </Routes>
      </div>
    </Router>
  );
};


export default App;
