
import React, { useState, useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';

const POST_HEADERS = {
  'Content-Type': 'application/json',
  'Accepts': 'application/json'
}

const URL = "/api/v1"

export default function App() {

  const navigate = useNavigate()
  const [currentUser, setCurrentUser] = useState(

  );

  useEffect( () => {
    fetch(URL + '/check_session')
    .then((response) => {
      if (response.ok) {
        response.json()
    .then((data) => {
      setCurrentUser(data)
      const role = data.role;

      if (role === 'clinic_admin') {navigate('/clinic-dashboard')}
      else if (role === 'patient') {navigate('/patient-dashboard')}
    })
      } else {navigate('/landing')}
    })
  }, [navigate]) 

  async function attemptLogin(userInfo) {
    const res = await fetch(URL + '/login', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify(userInfo)
    })
    if (res.ok) {
      const data = await res.json();
      setCurrentUser(data);
      return data
    } 
    else {
      alert('Invalid login');
      return false;
    }
  }

  async function attemptClinicSignup(userInfo) {
    try {
    const res = await fetch(URL + '/clinic_admin-registration', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify(userInfo)
    })
    if (res.ok) {
      const data = await res.json();
      setCurrentUser(data);
    } else {
      alert('Invalid sign up')
    }
  } catch (error){
    alert(error)
  }
  }

  function logout() {
    setCurrentUser(null)
    fetch(URL + '/logout', {
      method: 'DELETE'
    })

    navigate('/landing')
  }



  return (
    <>
      <Outlet context={{ currentUser, attemptLogin, attemptClinicSignup, logout }} />
    </>
  );
}
