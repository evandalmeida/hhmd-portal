import { useState, useEffect } from 'react';
import axios from 'axios';

function AppointmentForm() {
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState('');

  useEffect(() => {
    axios.get('/available_slots')
      .then(res => {
        setSlots(res.data);
      })
      .catch(err => console.log(err));
  }, []);

  const handleSlotChange = e => {
    setSelectedSlot(e.target.value);
  }
  
  const handleSubmit = () => {
    axios.post('/book_appointment', {
      slotId: selectedSlot
    })
      .then(res => {
        console.log('Appointment booked!');
        setSelectedSlot('');
      })
      .catch(err => console.log(err));
  }

  return (
    <div>
      <select value={selectedSlot} onChange={handleSlotChange}>
        <option>Select appointment slot</option>
        {slots.map(slot => (
          <option key={slot.id} value={slot.id}>
            {slot.date} @ {slot.time}  
          </option>
        ))}
      </select>

      <button onClick={handleSubmit}>Book Appointment</button>
    </div>
  );
}

export default AppointmentForm;