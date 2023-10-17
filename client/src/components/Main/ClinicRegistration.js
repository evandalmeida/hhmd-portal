// ClinicRegistration.js
import React, { useState } from 'react';

const ClinicRegistration = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [clinicName, setClinicName] = useState('');
  const [clinicAddress, setClinicAddress] = useState('');
  const [clinicState, setClinicState] = useState('');
  const [clinicZipCode, setClinicZipCode] = useState('');
  const [error, setError] = useState('');

  const handleRegistration = async () => {
    try {
      // Send a POST request to your server for clinic registration
      const response = await fetch('/clinic_register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          clinic_name: clinicName,
          clinic_address: clinicAddress,
          clinic_state: clinicState,
          clinic_zip_code: clinicZipCode,
        }),
      });

      if (response.status === 200) {
        // Successful clinic registration
        // Redirect to the login page or show a success message
        alert('Clinic registration successful. You can now log in.');
        // You can use react-router-dom to navigate to the login page
      } else {
        // Handle registration error
        setError('User with this email already exists');
      }
    } catch (error) {
      console.error('Clinic registration error:', error);
      setError('An error occurred during registration');
    }
  };

  return (
    <div>
      <h2>Clinic Registration</h2>
      <div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Clinic Name"
          value={clinicName}
          onChange={(e) => setClinicName(e.target.value)}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Clinic Address"
          value={clinicAddress}
          onChange={(e) => setClinicAddress(e.target.value)}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Clinic State"
          value={clinicState}
          onChange={(e) => setClinicState(e.target.value)}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Clinic Zip Code"
          value={clinicZipCode}
          onChange={(e) => setClinicZipCode(e.target.value)}
        />
      </div>
      {error && <p>{error}</p>}
      <button onClick={handleRegistration}>Register Clinic</button>
    </div>
  );
};

export default ClinicRegistration;
