import React from 'react';
import '../styles/Sidebar.css';

const darkBlue = "#080e2e";

const Sidebar = ({ toggleFiles }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-item">
        <img src="/assets/CStarLogo.png" alt="Logo" />
      </div>

      <div className="sidebar-item" onClick={toggleFiles}>
        <img src="/assets/folder.png" alt="Files" />
      </div>

      <div
        className="sidebar-item"
        onClick={() => alert('Terminal clicked')} 
      >
        <img src="/assets/terminal.png" alt="Terminal" />
      </div>
    </div>
  );
};

export default Sidebar;
