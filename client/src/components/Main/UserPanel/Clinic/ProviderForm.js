
import { useOutletContext } from 'react-router-dom';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';


export default function ProvidersForm() {

    const { currentUser, logout } = useOutletContext();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
      first_name: "",
      last_name: "",
      provider_type: null
    });

    
    const handleChange = (e) => {
    setFormData({
        ...formData,
        [e.target.name]: e.target.value
    });
    }
  
    const handleSubmit = async (e) => {
        e.preventDefault();
      
        const res = await fetch('/new_providers', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json', // Set the content type to JSON
          },
          body: JSON.stringify(formData),
        });
      
        if (res.ok) {
          // redirect back to dashboard
          navigate('/clinic-dashboard'); 
        }
      }
      

    const handleHome = (e) => {
        navigate('/clinic-dashboard')
    }
  
    return (
        <>
            <div className='provider-panel'>
                <h3 className='provider'>Add Provider</h3>
                <div className='provider-buttons'>
                    <button onClick={handleHome} className='home'>Home</button>
                    <br/>
                    <button onClick={logout} className='logout'>Logout</button>
                    <br/>
                </div>
                <br/>
            </div>
            <form onSubmit={handleSubmit} className='provider-form'>

            <input 
                name="first_name"
                value={formData.first_name}
                placeholder='Enter First Name'
                onChange={handleChange} 
            />

            <input
                name="last_name"
                value={formData.last_name}
                placeholder='Enter Last Name'
                onChange={handleChange}
            />  

            <select 
                name="provider_type"
                value={formData.provider_type}
    
                onChange={handleChange}
            >
                <option value="null">-- select from below --</option>
                <option value="MD">MD</option>
                <option value="DO">DO</option>
                <option value="PA">PA</option>
                <option value="NP">NP</option>
            </select>

            <button type="submit">Add Provider</button>
        </form>
        </>
    )
  }
  