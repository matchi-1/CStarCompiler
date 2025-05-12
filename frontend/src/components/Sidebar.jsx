import React from 'react';
import '../styles/Sidebar.css';

const Sidebar = ({ toggleFiles }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <img src="/assets/CStarLogo1.png" alt="Logo" />
      </div>

      <div className="sidebar-item" onClick={toggleFiles}>
        <img src="/assets/folder.png" alt="Files" />
      </div>

      {/* <div
        className="sidebar-item"
        onClick={() => alert('Terminal clicked')}
      >
        {/*<img src="/assets/terminal.png" alt="Terminal" />
      </div> */}
    </div>
  );
};

export default Sidebar;
