import React, { useState } from "react";
import CreatorBible from "./CreatorBible";
import UploadCampaign from "./UploadCampaign";
import CreatorReachouts from "./CreatorReachouts";
import "../styles/WelcomePage.css";

const WelcomePage: React.FC = () => {
  const [activeSection, setActiveSection] = useState<
    "creator-bible" | "campaign-upload" | "creator-reach-outs"
  >("creator-bible");

  const renderContent = () => {
    switch (activeSection) {
      case "creator-bible":
        return <CreatorBible />;
      case "campaign-upload":
        return <UploadCampaign />;
      case "creator-reach-outs":
        return <CreatorReachouts />;
      default:
        return null;
    }
  };

  return (
    <div className="welcome-page">
      {/* Welcome Header Section */}
      <div className="welcome-header">
        <h2>Welcome, {localStorage.getItem("full_name") || "Guest"}!</h2>
      </div>

      {/* Toggle Buttons */}
      <div className="button-toggle-container">
        <button
          className={`toggle-button ${activeSection === "creator-bible" ? "active" : ""}`}
          onClick={() => setActiveSection("creator-bible")}
        >
          Creator Bible
        </button>
        <button
          className={`toggle-button ${activeSection === "campaign-upload" ? "active" : ""}`}
          onClick={() => setActiveSection("campaign-upload")}
        >
          Campaign Upload
        </button>
        <button
          className={`toggle-button ${activeSection === "creator-reach-outs" ? "active" : ""}`}
          onClick={() => setActiveSection("creator-reach-outs")}
        >
          Creator Reach Outs
        </button>
      </div>

      {/* Dynamic Content */}
      <div className="content-container">
        {renderContent()}
      </div>
    </div>
  );
};

export default WelcomePage;
