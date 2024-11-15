// App.tsx
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

  // Effect to navigate when loggedIn status changes
  useEffect(() => {
    if (loggedIn) {
      console.log("Navigating to welcome page...");
      if (loggedIn) {
        console.log("Navigating to welcome page...");
        navigate("/welcome");
      }
      navigate("/welcome");
    }
  }, [loggedIn, navigate]);

  const handleLoginSuccess = () => {
    console.log("Login successful! Updating loggedIn state...");
    setLoggedIn(true);
  };

  return (
    <div className="App">
      <Header />
      <Routes>
        {/* Public routes */}
        <Route
          path="/"
          element={
            isSignup ? (
              <SignUpForm setIsSignup={setIsSignup} />
            ) : (
              <LoginForm setIsSignup={setIsSignup} onLoginSuccess={handleLoginSuccess} />
            )
          }
        />
        
        {/* Protected routes */}
        <Route element={<ProtectedRoute loggedIn={loggedIn} />}>
          <Route path="/welcome" element={<WelcomePage />} />
          <Route path="/creator-bible" element={<CreatorBible />} />
          <Route path="/upload-campaign" element={<UploadCampaign />} />
          <Route path="/creator-history" element={<CreatorHistory />} />
        </Route>
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
