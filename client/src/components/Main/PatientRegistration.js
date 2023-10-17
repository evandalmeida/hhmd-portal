// PatientRegistration.js
import React, { useState } from 'react';

const PatientRegistration = () => {
  const [user, setUser] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '', // Add the additional fields here
    street_address: '',
    state: '',
    zip_code: '',
  });
  const [error, setError] = useState('');

  const handleRegistration = async () => {
    try {
      const response = await fetch('/patient_register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
      });

      if (response.status === 200) {
        // Successful patient registration
        // Redirect to the login page or show a success message
        alert('Registration successful. You can now log in.');
        // You can use react-router-dom to navigate to the login page
      } else if (response.status === 400) {
        // Handle registration error for missing or invalid fields
        const data = await response.json();
        setError(data.error);
      } else if (response.status === 409) {
        // Handle registration error for duplicate email
        setError('User with this email already exists');
      } else {
        // Handle other registration errors
        setError('An error occurred during registration');
      }
    } catch (error) {
      console.error('Patient registration error:', error);
      setError('An error occurred during registration');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUser({
      ...user,
      [name]: value,
    });
  };

  return (
    <div>
      <h2>Patient Registration</h2>
      <div>
        <input
          type="text"
          placeholder="Username"
          name="username"
          value={user.username}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <input
          type="email"
          placeholder="Email"
          name="email"
          value={user.email}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Password"
          name="password"
          value={user.password}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="First Name"
          name="first_name"
          value={user.first_name}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Last Name"
          name="last_name"
          value={user.last_name}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Street Address"
          name="street_address"
          value={user.street_address}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="State"
          name="state"
          value={user.state}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Zip Code"
          name="zip_code"
          value={user.zip_code}
          onChange={handleInputChange}
        />
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={handleRegistration}>Register Patient</button>
    </div>
  );
};

export default PatientRegistration;
