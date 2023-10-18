import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PatientDashboard = ({ currentUser }) => {
  const [patientInfo, setPatientInfo] = useState({});
  const [upcomingAppointments, setUpcomingAppointments] = useState([]);

  useEffect(() => {
    // Make API requests to get patient data and upcoming appointments
    axios.get(`/api/patient_info/${currentUser.id}`)
      .then((response) => {
        setPatientInfo(response.data);
      })
      .catch((error) => {
        console.error('Error fetching patient info', error);
      });

    axios.get(`/api/upcoming_appointments/${currentUser.id}`)
      .then((response) => {
        setUpcomingAppointments(response.data);
      })
      .catch((error) => {
        console.error('Error fetching upcoming appointments', error);
      });
  }, [currentUser.id]);

  return (
    <div>
      <h1>Welcome, {patientInfo.username}</h1>
      <p>Patient ID: {patientInfo.id}</p>
      <p>Email: {patientInfo.email}</p>

      <h2>Upcoming Appointments:</h2>
      <ul>
        {upcomingAppointments.map((appointment) => (
          <li key={appointment.id}>
            {appointment.date} at {appointment.time}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PatientDashboard;
