import React, { useEffect } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';



export default function LandingPage() {
  const navigate = useNavigate();
  const {currentUser} = useOutletContext() ?? {} ;


  useEffect(() => {
    if (currentUser && currentUser.user) {
      if (!currentUser) {
        return <p>Loading...</p> 
      }

      if (currentUser?.user?.role === 'clinic_admin') {
        navigate('/clinic-dashboard');

      } else if (currentUser?.user?.role === 'patient') {
        navigate('/patient-dashboard');
      } 

    }
    
  }, [currentUser, navigate]);


  return (
    <>
      {!currentUser ? (
        <>
          <div className='buttons'>
            <button className='homebutton' onClick={() => navigate('/clinic_admin-registration')}>
              Register as Clinic
            </button>
            <button className='homebutton' onClick={() => navigate('/patient-registration')}>
              Register as Patient
            </button>
            <button className='homebutton' onClick={() => navigate('/login')}>
              Login
            </button>
          </div>
        </>
      ) : null}
    </>
  );
};