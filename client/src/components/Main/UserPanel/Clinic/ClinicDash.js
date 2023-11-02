import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import Footer from '../../Footer'


const CBR = '/api/v1';

export default function ClinicDashboard() {
  const { currentUser, logout } = useOutletContext();
  const [providers, setProviders] = useState([]);
  const [clinicInfo, setClinicInfo] = useState({});
  const [patients, setPatients] = useState({});
  const [isLoading, setIsLoading] = useState(true);


  const [showProviders, setShowProviders] = useState(true);
  const [showPatients, setShowPatients] = useState(true);
  const [showClinicInfo, setShowClinicInfo] = useState(false);

  useEffect(() => {
    if (currentUser?.role === 'clinic_admin') {

      // Fetch clinic information
      fetch(CBR + '/clinic_info')
        .then((response) => {if (response.ok) {return response.json()}})
        .then((data) => {setClinicInfo(data)});

      // Fetch appointments
      fetch(CBR + '/providers')
        .then((response) => {if (response.ok) {return response.json()}})
        .then((data) => {setProviders(data)});

      // Fetch patients
      fetch(CBR + '/patients')
        .then((response) => {if (response.ok) {return response.json()}})
        .then((data) => {setPatients(data)})
        .finally(() => setIsLoading(false));
    }
  }, [currentUser]);

  const toggleProviders = () => {
    setShowProviders(!showProviders);
  };

  const togglePatients = () => {
    setShowPatients(!showPatients);
  };

  const toggleClinicInfo = () => {
    setShowClinicInfo(!showClinicInfo);
  };

  return (
    <div className="dash">
      <div className='clinic_dash'>
        <div className='dash-top'>
          <h2 onClick={toggleClinicInfo}>THIS CLINIC</h2>
          <div className='user_control'>
            <h3 className='user'>Welcome {clinicInfo?.name}</h3>
            <button onClick={logout} className='logout'>Logout</button>
          </div>
        </div>
        {showClinicInfo && (
          isLoading ? (
            <p>Loading clinic information...</p>
          ) : (
            <div className='clinic-info'>
              <p>Name: {clinicInfo.name}</p>
              <p>Address: {clinicInfo.address}</p>
              <p>State: {clinicInfo.state}</p>
              <p>Zip Code: {clinicInfo.zip_code}</p>
            </div>
          )
        )}
      </div>



      <div className='clinic_provider_dash'>
        <h2 onClick={toggleProviders} >ALL PROVIDERS</h2>
        {showProviders && (
          isLoading ? (
          <p>Loading providers...</p>
        ) : (
          <div className='providers'>
            <div className="table-wrapper" >
              <table >
                <thead>
                  <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Provider Type</th>
                  </tr>
                </thead>
                <tbody >
                  {providers.map((provider) => (
                    <tr key={provider.id}>
                      <td>{provider.first_name}</td>
                      <td>{provider.last_name}</td>
                      <td>{provider.provider_type}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      }
        
      </div>



      <div className='clinic_patient_dash'>
        <h2 onClick={togglePatients} >ALL PATIENTS</h2>
        {showPatients && (
          isLoading ? (
          <p>Loading patients...</p>
        ) : (
          <div className='patients'>
            <div className="table-wrapper">
              <table >
                <thead>
                  <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>DOB</th>
                  </tr>
                </thead>
                <tbody >
                  {patients.map((patient) => (
                    <tr key={patient.id}>
                      <td>{patient.first_name}</td>
                      <td>{patient.last_name}</td>
                      <td>{patient.dob}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      }
      </div>
      <Footer/>
    </div>
  );
}
