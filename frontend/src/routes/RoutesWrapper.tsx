import React from "react";
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginForm from "./components/LoginForm";
import WelcomePage from "./components/WelcomePage";

const RoutesWrapper: React.FC = () => {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route
          path="/welcome"
          element={<ProtectedRoute element={<WelcomePage />} />}
        />
      </Routes>
    </div>
  );
};

export default RoutesWrapper;
