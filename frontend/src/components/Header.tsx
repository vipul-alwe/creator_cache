import React from "react";
import "../styles/Header.css";
import logo from "../assets/logos/3.png";
import LogOutMenu from "./LogoutMenu";

interface HeaderProps {
  loggedIn: boolean;
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ loggedIn, onLogout }) => {
  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="Logo" />
      </div>
      {loggedIn && (
        <div className="user-menu">
          {/* Only display the LogOutMenu */}
          <LogOutMenu onLogout={onLogout} />
        </div>
      )}
    </header>
  );
};

export default Header;
