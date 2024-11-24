import React, { useState, useEffect } from "react";
import { Routes, Route, useNavigate, Navigate } from "react-router-dom";
import LoginForm from "./components/LoginForm";
import SignUpForm from "./components/SignUpForm";
import Header from "./components/Header";
import Footer from "./components/Footer";
import WelcomePage from "./components/WelcomePage";
import ProtectedRoute from "./components/ProtectedRoute";
import "./App.css";

const App: React.FC = () => {
  const [isSignup, setIsSignup] = useState(false);
  const [loggedIn, setLoggedIn] = useState(
    localStorage.getItem("loggedIn") === "true"
  );

  const navigate = useNavigate();

  useEffect(() => {
    // Redirect user to the appropriate route based on login state
    if (loggedIn) {
      console.log("User is already logged in. Redirecting to welcome page...");
      navigate("/welcome");
    }
  }, [loggedIn, navigate]);

  const handleLoginSuccess = (user: { full_name: string }) => {
    console.log("Login successful!");

    // Save user data to localStorage
    localStorage.setItem("full_name", user.full_name);
    localStorage.setItem("loggedIn", "true");

    // Set logged-in state and navigate to welcome page
    setLoggedIn(true);
  };

  const handleLogout = () => {
    console.log("Logging out...");
    // Clear localStorage and state
    localStorage.removeItem("loggedIn");
    localStorage.removeItem("full_name");
    setLoggedIn(false);

    // Redirect to login page
    navigate("/");
  };

  return (
    <div className="App">
      {/* Pass `loggedIn` state and `handleLogout` to Header */}
      <Header
        loggedIn={loggedIn}
        fullName={localStorage.getItem("full_name")}
        onLogout={handleLogout}
      />
      <Routes>
        {/* Public routes */}
        <Route
          path="/"
          element={
            loggedIn ? (
              <Navigate to="/welcome" replace />
            ) : isSignup ? (
              <SignUpForm setIsSignup={setIsSignup} />
            ) : (
              <LoginForm
                setIsSignup={setIsSignup}
                onLoginSuccess={handleLoginSuccess}
              />
            )
          }
        />
        <Route
          path="/signup"
          element={
            loggedIn ? (
              <Navigate to="/welcome" replace />
            ) : (
              <SignUpForm setIsSignup={setIsSignup} />
            )
          }
        />

        {/* Protected routes */}
        <Route element={<ProtectedRoute loggedIn={loggedIn} />}>
          <Route
            path="/welcome"
            element={<WelcomePage onLogout={handleLogout} />}
          />
        </Route>

        {/* Fallback for unknown routes */}
        <Route
          path="*"
          element={<Navigate to={loggedIn ? "/welcome" : "/"} replace />}
        />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
