

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios'; // Import Axios for making HTTP requests

const PatientDashboard = () => {
  const [patientInfo, setPatientInfo] = useState({});
  const [upcomingAppointments, setUpcomingAppointments] = useState([]);

  useEffect(() => {
    // Make API requests to get patient data and upcoming appointments
    axios.get('/api/patient_info')
      .then(response => {
        setPatientInfo(response.data); // Assuming you have an API endpoint /api/patient_info
      })
      .catch(error => {
        console.error('Error fetching patient info', error);
      });

    axios.get('/api/upcoming_appointments')
      .then(response => {
        setUpcomingAppointments(response.data); // Assuming you have an API endpoint /api/upcoming_appointments
      })
      .catch(error => {
        console.error('Error fetching upcoming appointments', error);
      });
  }, []);

  return (
    <div>
      <h1>Welcome, {patientInfo.username}</h1>
      <p>Patient ID: {patientInfo.id}</p>
      <p>Email: {patientInfo.email}</p>

      <h2>Upcoming Appointments:</h2>
      <ul>
        {upcomingAppointments.map(appointment => (
          <li key={appointment.id}>
            {appointment.date} at {appointment.time}
          </li>
        ))}
      </ul>

      <Link to="/schedule-appointment">Schedule New Appointment</Link>
      <Link to="/patient-profile">View Profile</Link>
    </div>
  );
};

export default PatientDashboard;
