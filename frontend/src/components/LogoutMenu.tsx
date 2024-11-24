import React, { useState } from "react";
import "../styles/LogoutMenu.css";

interface LogoutMenuProps {
  onLogout: () => void;
}

const LogoutMenu: React.FC<LogoutMenuProps> = ({ onLogout }) => {
  const [menuVisible, setMenuVisible] = useState(false);

  const toggleMenu = () => setMenuVisible((prev) => !prev);

  const fullName = localStorage.getItem("full_name") || "User";

  return (
    <div className="logout-menu-container">
      {/* Display user name only as the dropdown toggle */}
      <div className="user-name" onClick={toggleMenu}>
        {fullName}
      </div>
      {/* Dropdown appears only when menuVisible is true */}
      {menuVisible && (
        <div className="logout-dropdown">
          <button className="dropdown-item" onClick={onLogout}>
            Log Out
          </button>
        </div>
      )}
    </div>
  );
};

export default LogoutMenu;
