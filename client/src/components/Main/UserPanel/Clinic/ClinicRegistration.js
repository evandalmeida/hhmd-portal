import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ClinicRegistration = ({attemptClinicSignup}) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [clinicName, setClinicName] = useState('');
  const [clinicAddress, setClinicAddress] = useState('');
  const [clinicState, setClinicState] = useState('');
  const [clinicZipCode, setClinicZipCode] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username || !email || !password || !clinicName || !clinicAddress || !clinicState || !clinicZipCode) {
      setError('Please fill in all the required fields.');
      return;
    }

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

    try {
      const response = await attemptClinicSignup(registrationData);

      if (response.ok) {
        navigate('/login');
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Registration failed');
      }
    } catch (error) {
      setError('An error occurred during registration.');
    }
  };

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
        {error && <p className="error-message">{error}</p>}
        <button type="submit">Register Clinic</button>
      </form>
    </div>
  );
};

export default ClinicRegistration;