import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ClinicRegistration = ({ setCurrentUser }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [clinicName, setClinicName] = useState('');
  const [clinicAddress, setClinicAddress] = useState('');
  const [clinicState, setClinicState] = useState('');
  const [clinicZipCode, setClinicZipCode] = useState('');
  const [error, setError] = useState('');

  const handleRegistration = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5555/clinic_admin-registration', {
        method: 'POST',
        body: JSON.stringify({
          username: username,
          email: email,
          password: password,
          clinic_name: clinicName,
          clinic_address: clinicAddress,
          clinic_state: clinicState,
          clinic_zip_code: clinicZipCode,
        }),
      });
      

      if (response.status === 200) {
        setCurrentUser({ role: 'clinic_admin' });
        navigate('/clinic-dashboard');
      } else if (response.status === 409) {
        setError('Email already exists');
      } else {
        setError('Error registering clinic');
        console.error('Error:', response.status, response.statusText);
      }
    } catch (err) {
      console.error('Request Error:', err);
      setError('Error registering clinic');
    }
  };

  return (
    <div className="form">
      <h2 className="heading">Clinic Registration</h2>
      <form onSubmit={handleRegistration}>
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
          autoComplete="current-password"
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
        {error && <p className="error-message">{error}</p>}
        <button type="submit">Register Clinic</button>
      </form>
    </div>
  );
};

export default ClinicRegistration;
