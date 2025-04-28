import React, { useEffect } from 'react';
import '../styles/Header.css';
import { io } from 'socket.io-client';

const socket = io("http://localhost:5000");
// const socket = io("https://cstar-backend-217043973303.asia-southeast1.run.app", {
//   transports: ["websocket"],
//   secure: true
// });

const Header = ({ editorRef, fileData, activeTab, clickHandler, clearLogs, onExecutionComplete }) => {

  const handleTerminate = () => {
    console.log("Terminating program...");
    socket.emit("terminate_runtime");
    onExecutionComplete()
  };


  useEffect(() => {
    console.log(">>>>> [from header.jsx] PROGRAM STILL RUNNING? " + clearLogs)
  }, [clearLogs]);

  // Undo functionality
  const handleUndo = () => {
    if (editorRef.current) {
      editorRef.current.trigger('keyboard', 'undo', null);
    }
  };

  // Redo functionality
  const handleRedo = () => {
    if (editorRef.current) {
      editorRef.current.trigger('keyboard', 'redo', null);
    }
  };

  const handleDownload = () => {
    const file = fileData.find((file) => file.name === activeTab);
    if (file) {
      const blob = new Blob([file.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = file.name; // Use file name for the download
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } else {
      alert('No file selected for download.');
    }
  };

  return (
    <div className="header">
      <div className='header-menu'>
        <div className="header-item" onClick={handleUndo}>
          <p>Undo</p>
        </div>
        <div className="header-item" onClick={handleRedo}>
          <p>Redo</p>
        </div>
        <div className="header-item">
          <p>Save</p>
        </div>
        <div className="header-item" onClick={handleDownload}>
          <p>Download</p>
        </div>
      </div>

      <div className='header-btns'>
        <div className={`img-btn-wrapper ${clearLogs ? 'disabled' : ''}`} onClick={clickHandler}>
          <img src="/assets/run-btn.png" alt="run-btn" />
        </div>

        <div className={`stop-btn-wrapper ${!clearLogs ? 'disabled' : ''}`} onClick={handleTerminate}>
          <img src="/assets/stop-btn.png" alt="stop-btn" />
        </div>
      </div>

    </div>
  );
};

export default Header;
