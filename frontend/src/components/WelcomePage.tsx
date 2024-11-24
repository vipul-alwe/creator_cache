// WelcomePage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";

const WelcomePage: React.FC<{ onLogout: () => void }> = ({ onLogout }) => {
  const navigate = useNavigate();

  return (
    <div className="welcome">
      <h2>Welcome, {localStorage.full_name}</h2>
      <div className="button-container">
        <button onClick={() => navigate("/creator-bible")}>View Creator Bible</button>
        <button onClick={() => navigate("/upload-campaign")}>Upload Campaign</button>
        <button onClick={() => navigate("/creator-history")}>Creator History</button>
      </div>
    </div>
  );
};

export default WelcomePage;
