import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = ({ isLoggedIn, onLogout }) => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        {isLoggedIn ? (
          <React.Fragment>
            <li>
              <Link to="/dashboard">Dashboard</Link>
            </li>
            <li>
              <Link to="/profile">Profile</Link>
            </li>
            <li>
              <button onClick={onLogout}>Logout</button>
            </li>
          </React.Fragment>
        ) : (
          <React.Fragment>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/clinic-registration">Clinic Registration</Link>
            </li>
            <li>
              <Link to="/patient-registration">Patient Registration</Link>
            </li>
          </React.Fragment>
        )}
      </ul>
    </nav>
  );
};

export default NavBar;
