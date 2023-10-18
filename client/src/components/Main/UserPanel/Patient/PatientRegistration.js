import React, { useState } from 'react';

const PatientRegistration = () => {
  const [user, setUser] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    street_address: '',
    state: '',
    zip_code: '',
    dob: '', // Add the date of birth field
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
    <div className='form'>
      <h2 className='heading'>Patient Registration</h2>
      <form>
        <input
          type="text"
          placeholder="Username"
          name="username"
          value={user.username}
          onChange={handleInputChange}
        />

        <input
          type="email"
          placeholder="Email"
          name="email"
          value={user.email}
          onChange={handleInputChange}
        />

        <input
          type="password"
          placeholder="Password"
          name="password"
          value={user.password}
          onChange={handleInputChange}
        />

        <input
          type="text"
          placeholder="First Name"
          name="first_name"
          value={user.first_name}
          onChange={handleInputChange}
        />

        <input
          type="text"
          placeholder="Last Name"
          name="last_name"
          value={user.last_name}
          onChange={handleInputChange}
        />

        <input
          type="text"
          placeholder="Street Address"
          name="street_address"
          value={user.street_address}
          onChange={handleInputChange}
        />

        <input
          type="text"
          placeholder="State"
          name="state"
          value={user.state}
          onChange={handleInputChange}
        />

        <input
          type="text"
          placeholder="Zip Code"
          name="zip_code"
          value={user.zip_code}
          onChange={handleInputChange}
        />
        <input
            type="date"
            placeholder="Date of Birth"
            name="dob"
            value={user.dob}
            onChange={handleInputChange}
            style={{ fontFamily: 'sans-serif' }} // Change the font here
          />
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={handleRegistration}>Register Patient</button>
    </div>
  );
};

export default PatientRegistration;
