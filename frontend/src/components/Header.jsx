import React from 'react';
import '../styles/Header.css';

const Header = ({ editorRef }) => {
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
    console.log("downloading..");
    //add later
  };
  return (
    <div className="header">
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
  );
};

export default Header;
