import React from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate instead of useHistory

const WelcomePage: React.FC = () => {
  const navigate = useNavigate(); // Replace useHistory with useNavigate

  return (
    <div className="welcome">
      <h2>Welcome, Full Name</h2>
      <div className="button-container">
        <button onClick={() => navigate("/creator-bible")}>View Creator Bible</button>
        <button onClick={() => navigate("/upload-campaign")}>Upload Campaign</button>
        <button onClick={() => navigate("/creator-history")}>Creator History</button>
      </div>
    </div>
  );
};

export default WelcomePage;
