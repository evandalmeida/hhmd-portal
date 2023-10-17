import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Login from './Main/Login';
import PatientRegistration from './Main/PatientRegistration';
import ClinicRegistration from './Main/ClinicRegistration';

const App = () => {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/patient-registration" component={PatientRegistration} />
          <Route path="/clinic-registration" component={ClinicRegistration} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;