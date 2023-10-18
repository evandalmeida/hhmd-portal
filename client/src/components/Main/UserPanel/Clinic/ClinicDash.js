import React, { useState, useEffect } from 'react';

export default function ClinicDashboard({ currentUser, logout }) {
  const [appointments, setAppointments] = useState([]);
  const [clinicInfo, setClinicInfo] = useState({});
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    if (currentUser.user?.role === "clinic_admin") {
      // Define headers with JWT token
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentUser.access_token}` // Assuming the token is stored in currentUser.access_token
      };

      // Fetch clinic info with headers
      fetch('/clinic_info', { headers })
        .then((response) => response.json())
        .then((data) => setClinicInfo(data)) // Update the clinicInfo state

      // Fetch appointments with headers
      fetch('/appointments', { headers })
        .then((response) => response.json())
        .then((appointments) => setAppointments(appointments)) // Update the appointments state

      // Fetch patients with headers
      fetch('/patients', { headers })
        .then((response) => response.json())
        .then((patients) => setPatients(patients)) // Update the patients state
    }
  }, [currentUser]);

  if (currentUser.user?.role === "clinic_admin") {
    return (
      <div>
        <h2>Clinic Information</h2>
        <button className='logout' onClick={logout}>Logout</button> 
        <p>Name: {clinicInfo.name}</p>
        <p>Address: {clinicInfo.address}</p>
        <p>State: {clinicInfo.state}</p>
        <p>Zip Code: {clinicInfo.zip_code}</p>

        <h2>Appointments</h2>
        <ul>
          {appointments.map((appointment) => (<li key={appointment.id}>Date: {appointment.date}, Time: {appointment.time}</li>))}
        </ul>

        <h2>Patients</h2>
        <ul>
          {patients.map((patient) => (<li key={patient.id}>Name: {patient.first_name} {patient.last_name}, DOB: {patient.dob}</li>))}
        </ul>
      </div>
    );
  } else {
    return <p>Null or whatever idk</p>
  }
}
