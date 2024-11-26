import React from 'react';

// colors
const darkBlue = "#080e2e";

const Sidebar = ({ toggleFiles }) => {
  return (
    <div
      className="sidebar"
      style={{
        width: '55px',
        height: '100vh',
        backgroundColor: darkBlue, 
        color: '#fff',
        position: 'fixed',
        top: '0',
        left: '0',
        paddingTop: '15px', 
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      {/* Logo Image */}
      <div
        className="sidebar-item"
        style={{
          marginBottom: '35px',
          cursor: 'pointer',
        }}
      >
        <img 
          src="/assets/CStarLogo.png" 
          alt="Logo"
          style={{
            width: '36px',
            height: '36px',
          }}
        />
      </div>

      {/* Files Icon */}
      <div
        className="sidebar-item"
        onClick={toggleFiles}
        style={{
          padding: '10px',
          marginBottom: '10px',
          cursor: 'pointer',
        }}
      >
        <img 
          src="/assets/folder.png"
          alt="Files"
          style={{
            width: '25px',
            height: '25px',
          }}
        />
      </div>

      {/* Terminal Icon */}
      <div
        className="sidebar-item"
        style={{
          padding: '10px',
          marginBottom: '10px',
          cursor: 'pointer',
        }}
        onClick={() => alert('Terminal clicked')} 
      >
        <img 
          src="/assets/terminal.png" 
          alt="Terminal"
          style={{
            width: '25px',
            height: '25px',
          }}
        />
      </div>
    </div>
  );
};

export default Sidebar;
