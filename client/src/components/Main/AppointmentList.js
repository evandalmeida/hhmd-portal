import { useState, useEffect } from 'react';
import axios from 'axios';

function AppointmentList() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    axios.get('/appointments')
      .then(res => {
        setAppointments(res.data);
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <div>
      {appointments.map(appt => (
        <div key={appt.id}>
          {appt.slot.date} @ {appt.slot.time}
        </div>  
      ))}
    </div>
  );
}

export default AppointmentList;