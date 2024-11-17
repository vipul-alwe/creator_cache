import React, { useState, useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import LoginForm from "./components/LoginForm";
import SignUpForm from "./components/SignUpForm";
import Header from "./components/Header";
import Footer from "./components/Footer";
import WelcomePage from "./components/WelcomePage";
import CreatorBible from "./components/CreatorBible";
import UploadCampaign from "./components/UploadCampaign";
import CreatorHistory from "./components/CreatorHistory";
import ProtectedRoute from "./components/ProtectedRoute";
import "./App.css";

const App: React.FC = () => {
  const [isSignup, setIsSignup] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    console.log("useEffect triggered. loggedIn state:", loggedIn); // Debugging log
    if (loggedIn) {
      console.log("Logged in successfully, navigating to /welcome..."); // Debugging log
      navigate("/welcome"); // Navigate to the welcome page
    }
  }, [loggedIn, navigate]);

  const handleLoginSuccess = () => {
    console.log("handleLoginSuccess called. Setting loggedIn to true."); // Debugging log
    setLoggedIn(true); // Update the loggedIn state
  };

  return (
    <div className="App">
      <Header />
      <Routes>
        {/* Public routes */}
        <Route>
          path="/"
          element={
            isSignup ? (
              <SignUpForm setIsSignup={setIsSignup} />
            ) : (
              <LoginForm setIsSignup={setIsSignup} onLoginSuccess={handleLoginSuccess} />
              
            )
          }
          <Route path="" element={<WelcomePage />} />
        </Route>
        {/* <Route path="/welcome" element={<ProtectedRoute loggedIn={loggedIn} />} >
        <Route path="" element={<WelcomePage />} />
        </Route> */}

        {/* Protected routes */}
        {/* <Route element={<ProtectedRoute loggedIn={loggedIn} />}>
          <Route path="/welcome" element={<WelcomePage />} />
          <Route path="/creator-bible" element={<CreatorBible />} />
          <Route path="/upload-campaign" element={<UploadCampaign />} />
          <Route path="/creator-history" element={<CreatorHistory />} />
        </Route> */}
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
