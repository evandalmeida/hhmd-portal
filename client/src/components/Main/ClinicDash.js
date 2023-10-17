import { useState, useEffect } from 'react';
import axios from 'axios';

function ClinicDashboard() {

  const [slots, setSlots] = useState([]);

  useEffect(() => {
    axios.get('/available_slots')
     .then(res => {
       setSlots(res.data);
     })
     .catch(err => console.log(err));
  }, []);

  return (
    <div>
      <h2>Available Slots</h2>
      {slots.map(slot => (
        <div key={slot.id}>
          {slot.date} @ {slot.time}
        </div>
      ))}
    </div>
  );
}

export default ClinicDashboard;