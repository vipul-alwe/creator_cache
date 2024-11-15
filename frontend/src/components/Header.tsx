import React from "react";
import "../styles/Header.css"; // Ensure the CSS file is created for styling
import logo from "../assets/logo.svg"; // Import the logo from the assets folder

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="Logo" /> {/* Use the imported logo */}
        <h1>Creator Cache</h1>
      </div>
    </header>
  );
};

export default Header;
