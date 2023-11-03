import ReactDOM from 'react-dom/client'; 
import React from "react";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom"

// COMPONENTS
import App from "./components/App";
import ClinicRegistration from "./components/Main/UserPanel/Clinic/ClinicRegistration"; 
import PatientRegistration from "./components/Main/UserPanel/Patient/PatientRegistration";
import ClinicDashboard from "./components/Main/UserPanel/Clinic/ClinicDash";
import ProviderForm from "./components/Main/UserPanel/Clinic/ProviderForm";
import PatientDashboard from "./components/Main/UserPanel/Patient/PatientDash";
import Login from "./components/Main/UserPanel/Login";
import LandingPage from "./components/Main/LandingPage"

const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>,
        children: [
            {
                path: "/landing",
                index: true,
                element: <LandingPage/>,
            },
            {
                path: "/clinic_admin-registration",
                element: <ClinicRegistration/>,
            },
            {
                path: "/patient-registration",
                element: <PatientRegistration/>,
            },
            {
                path: "login",
                element: <Login/>,
            },
            {
                path: '/clinic-dashboard',
                element: <ClinicDashboard/>,
            },
            {
                path: '/patient-dashboard',
                element: <PatientDashboard/>,
            },
            {
                path: '/providers/new',
                element: <ProviderForm/>,
            }
        ]
    }
])

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(<RouterProvider router={router}/>);