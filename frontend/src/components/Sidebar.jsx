import React from 'react';

// colors
const darkBlue = "#1c416b";

const Sidebar = () => {
  return (
    <div
      className="sidebar"
      style={{
        width: '55px',
        height: '94.5vh',
        backgroundColor: darkBlue, 
        color: '#fff',
        position: 'fixed',
        top: '0',
        left: '0',
        paddingTop: '15px', 
        margin: '6px',
        borderRadius: '9px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      {/* Logo Image */}
      <div
        className="sidebar-item"
        style={{
          marginBottom: '20px',
          cursor: 'pointer',
        }}
      >
        <img 
          src="/assets/CStarLogo.png" 
          alt="Logo"
          style={{
            width: '38px',
            height: '38px',
          }}
        />
      </div>

      {/* Files Icon */}
      <div
        className="sidebar-item"
        style={{
          padding: '10px',
          marginBottom: '10px',
          cursor: 'pointer',
        }}
        onClick={() => alert('Files clicked')} 
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
