// ProtectedRoute.tsx
import React from "react";
import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
  loggedIn: boolean;
  children: React.ReactNode; // Make sure children prop is typed correctly
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ loggedIn, children }) => {
  if (!loggedIn) {
    return <Navigate to="/" />; // Redirect to login if not logged in
  }

  return <>{children}</>; // Render children if logged in
};

export default ProtectedRoute;
