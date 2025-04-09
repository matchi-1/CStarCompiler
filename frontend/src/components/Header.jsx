import React, { useEffect } from 'react';
import '../styles/Header.css';

const Header = ({ editorRef, fileData, activeTab, clickHandler, clearLogs, onExecutionComplete }) => {

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

        <div className='stop-btn-wrapper' onClick={clickHandler}>
          <img src="/assets/stop-btn.png" alt="stop-btn" />
        </div>
      </div>

    </div>
  );
};

export default Header;
