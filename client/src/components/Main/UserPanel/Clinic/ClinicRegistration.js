import React, { useState } from 'react';
import { useNavigate, useOutletContext} from 'react-router-dom';

export default function ClinicRegistration() {

  const navigate = useNavigate();
  const {attemptClinicSignup} = useOutletContext()

  const [email, setEmail] = useState('');
  // eslint-disable-next-line
  const [error, setError] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [clinicName, setClinicName] = useState('');
  const [clinicState, setClinicState] = useState('');
  const [clinicZipCode, setClinicZipCode] = useState('');
  const [clinicAddress, setClinicAddress] = useState('');


  async function handleSubmit(e) {
    e.preventDefault()
    

    try {
    const registrationData = {
      username,
      email,
      password,
      clinic_name: clinicName,
      clinic_address: clinicAddress,
      clinic_state: clinicState,
      clinic_zip_code: clinicZipCode,
      role:'clinic_admin',
    };

    const registrationSuccess = await attemptClinicSignup(registrationData);



    if (registrationSuccess) {
      navigate('/clinic-dashboard')
      } else {
        setError('Invalid');
      }
  } catch (error) {
    console.error('Registration error:', error);
    setError('An error occurred during registration');
    navigate('/clinic_admin-registration')
  }
  }

  return (
    <div className="form">
      <h2 className="heading">Clinic Registration</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="new-password"
        />
        <input
          type="text"
          placeholder="Clinic Name"
          value={clinicName}
          onChange={(e) => setClinicName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Clinic Address"
          value={clinicAddress}
          onChange={(e) => setClinicAddress(e.target.value)}
        />
        <input
          type="text"
          placeholder="Clinic State"
          value={clinicState}
          onChange={(e) => setClinicState(e.target.value)}
        />
        <input
          type="text"
          placeholder="Clinic Zip Code"
          value={clinicZipCode}
          onChange={(e) => setClinicZipCode(e.target.value)}
        />
        <button type="submit">Register Clinic</button>
      </form>
    </div>
  );
}