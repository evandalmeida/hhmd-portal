import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';



const CBR = '/api/v1';

export default function ClinicDashboard() {

  const { currentUser, logout } = useOutletContext();
  const navigate = useNavigate();


  const [providers, setProviders] = useState([]);
  const [clinicInfo, setClinicInfo] = useState({});
  const [patients, setPatients] = useState({});
  const [isLoading, setIsLoading] = useState(true);


  const [showProviders, setShowProviders] = useState(true);
  const [showPatients, setShowPatients] = useState(true);
  const [showClinicInfo, setShowClinicInfo] = useState(false);
  const [deletingPatient, setDeletingPatient] = useState(null);
  const [deletingProvider, setDeletingProvider] = useState(null); 




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

  const toggleProviders = (e) => {
    setShowProviders(!showProviders);
  };

  const togglePatients = (e) => {
    setShowPatients(!showPatients);
  };

  const toggleClinicInfo = (e) => {
    setShowClinicInfo(!showClinicInfo);
  };

  const handleAddProvider = (e) => {
    navigate('/providers/new'); 
  }
  

  const handleDeleteProvider = async (id) => {
    setDeletingProvider(id);
    try {
      await fetch(`${CBR}/providers/${id}`, {
        method: 'DELETE'
      });
      setProviders(providers.filter(p => p.id !== id)); 
    } catch (err) {
      console.error(err);
    }
    setDeletingProvider(null);
  }

// Delete patient handler
  const handleDeletePatient = async (id) => {
    setDeletingPatient(id);
    try {
      await fetch(`${CBR}/patients/${id}`, {
        method: 'DELETE'
      });
      setPatients(patients.filter(p => p.id !== id));
    } catch (err) {
      console.error(err);
    }
    setDeletingPatient(null);
  }





  return (
    <div className="dash">
      <div className='clinic_dash'>
        <div className='dash-top'>
          <h2 onClick={toggleClinicInfo}>THIS CLINIC</h2>
          <div className='user_control'>
            <h3 className='user'>Welcome {clinicInfo?.name}</h3>
            <button onClick={logout} className='logout'>logout</button>
          </div>
        </div>
        {showClinicInfo && (
          isLoading ? (
            <p>Loading clinic information...</p>
          ) : (
            <div className='clinic-info'>
              <p>Your Clinc: {clinicInfo.name}</p>
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
                      <th>Remove Patient</th>
                    </tr>
                  </thead>
                  <tbody >
                    {providers.map((provider) => (
                      <tr key={provider.id}>
                        <td>{provider.first_name}</td>
                        <td>{provider.last_name}</td>
                        <td>{provider.provider_type}</td>
                        <td>
                          <button
                              className='delete-button'
                              disabled={deletingProvider === provider.id} 
                              onClick={() => handleDeleteProvider(provider.id)}
                            >
                              {deletingProvider === provider.id ? 'Deleting...' : 'Delete'}
                            </button>
                          </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                
              </div>
              <button className='provider-add-button' onClick={handleAddProvider}> Add a New Provider </button>
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
                      <th>Remove Patient</th>
                    </tr>
                  </thead>
                  <tbody >
                    {patients.map((patient) => (
                      <tr key={patient.id}>
                        <td>{patient.first_name}</td>
                        <td>{patient.last_name}</td>
                        <td>{patient.dob}</td>
                        <td>
                          <button 
                              className='delete-button'
                              disabled={deletingPatient === patient.id}
                              onClick={() => handleDeletePatient(patient.id)}
                            >
                              {deletingPatient === patient.id ? 'Deleting...' : 'Delete'}  
                            </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))
        }
      </div>
  
    </div>

  );
}


