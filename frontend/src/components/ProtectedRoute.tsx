import React from "react";
import { Navigate, Outlet } from "react-router-dom";

interface ProtectedRouteProps {
  loggedIn: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ loggedIn }) => {
  if (!loggedIn) {
    console.log("Access denied. Redirecting to login...");
    return <Navigate to="/" />;
  }
  return <Outlet />;
};

export default ProtectedRoute;
