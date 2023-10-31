import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';

export default function ClinicDashboard() {
  const { currentUser, logout } = useOutletContext();
  const [appointments, setAppointments] = useState([]);
  const [clinicInfo, setClinicInfo] = useState({});
  const [patients, setPatients] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  console.log(currentUser)

  useEffect(() => {
    if (currentUser?.user?.role === 'clinic_admin') {
      // Fetch clinic information
      fetch(URL + '/clinic_info')
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Failed to fetch clinic info');
          }
        })
        .then((data) => setClinicInfo(data))
        .catch((error) => console.error('Error fetching clinic info: ', error));

      // Fetch appointments
      fetch(URL + '/appointments')
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Failed to fetch appointments');
          }
        })
        .then((data) => setAppointments(data))
        .catch((error) => console.error('Error fetching appointments: ', error));

      // Fetch patients
      fetch(URL + '/patients')
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw Error('Failed to fetch patients');
          }
        })
        .then((data) => setPatients(data.patients))
        .catch((error) => console.error('Error fetching patients: ', error))
        .finally(() => setIsLoading(false));
    }
  }, [currentUser]);

  return (
    <div className="dash">
      <div>
        <button onClick={logout} className='logout'>Logout</button>
        <p>Welcome {currentUser?.id}</p>

      </div>
      <div>
        <h2>Your Clinic:</h2>
        {isLoading ? (
          <p>Loading clinic information...</p>
        ) : (
          <div>
            <p>Name: {clinicInfo.name}</p>
            <p>Address: {clinicInfo.address}</p>
            <p>State: {clinicInfo.state}</p>
            <p>Zip Code: {clinicInfo.zip_code}</p>
          </div>
        )}
      </div>

      <div>
        <h2>Appointments</h2>
        {isLoading ? (
          <p>Loading appointments...</p>
        ) : (
          <ul>
            {appointments.map((appointment) => (
              <li key={appointment.id}>
                Date: {appointment.date}, Time: {appointment.time}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <h2>Patients</h2>
        {isLoading ? (
          <p>Loading patients...</p>
        ) : (
          <ul>
            {patients.map((patient) => (
              <li key={patient.id}>
                Name: {patient.first_name} {patient.last_name}, DOB: {patient.dob}
              </li>
            ))}
          </ul>
        )}
      </div>

    </div>
  );
}
