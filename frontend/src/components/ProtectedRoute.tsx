import React from "react";
import { Navigate, Outlet } from "react-router-dom";

interface ProtectedRouteProps {
  loggedIn: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ loggedIn }) => {
  return loggedIn ? <Outlet /> : <Navigate to="/" />;
};

export default ProtectedRoute;
