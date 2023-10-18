import React, { useState, useEffect } from 'react';

export default function ClinicDashboard({ currentUser }) {
  const [appointments, setAppointments] = useState([]);
  const [clinicInfo, setClinicInfo] = useState({});
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    // clinic info
    fetch('http://localhost:5555/clinic_info')
    .then((response) => {
      if (!response.ok)
      return response.json()})
    .then((data) => {setClinicInfo(data)})

    // appointments
    fetch('http://localhost:5555/appointments')
    .then((response) => {
      if (!response.ok) 
      return response.json()})
    .then((data) => {setAppointments(data)})

    // patients
    fetch('http://localhost:5555/patients')
    .then((response) => {
      if (!response.ok) 
      return response.json()})
    .then((data) => {setPatients(data)})
  }, []);

  if (!currentUser){
    return (
      <div>
        <h2>Clinic Information</h2>
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
          {patients.map((patient) => (<li key={patient.id}>Name: {patient.first_name}+{patient.last_name}, DOB: {patient.dob}</li>))}
        </ul>
      </div>
    );
  }
}