import React, { useState } from "react";
import "./styles/styles.css"
import Camera from "./components/Camera";
import Home from "./components/Home";
import Navbar from "./components/Navbar";
import Verify from "./components/Verify";
import Register from "./components/Register";
import Alert from "./components/Alert";

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [showNavbar, setShowNavbar] = useState(true);

  const handleAccessCamera = () => {
    setCurrentPage('camera');
    setShowNavbar(false); // Hide navbar on Camera page
  };

  const handleAccessVerify = () => {
    setCurrentPage('verify');
    setShowNavbar(true); // Show navbar on Verify page
  };
  const handleAccessRegister = () => {
    setCurrentPage('register');
    setShowNavbar(true); // Show navbar on Register page
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
    setShowNavbar(true); // Show navbar on Home page
  };
  // const [showAlert, setShowAlert] = useState(true);

  

  return (
    <>
    
      

   
      {showNavbar && <Navbar onNavigateHome={handleBackToHome} onAccessRegister={handleAccessRegister} />}
      {currentPage === 'home' && (
        <Home onAccessCamera={handleAccessCamera} onAccessVerify={handleAccessVerify} />
      )}
      {currentPage === 'camera' && (
        <Camera onNavigateHome={handleBackToHome} />
      )}
      {currentPage === 'verify' && (
        <Verify />
      )}
      {currentPage === 'register' && (
        <Register onNavigateHome={handleBackToHome} />
      )}
    </>
  );
}

export default App;
