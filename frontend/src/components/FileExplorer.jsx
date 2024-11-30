import React from 'react';
import { FaFolder, FaFile } from 'react-icons/fa';
import { initializeApp } from "firebase/app";
import { IoIosArrowBack } from 'react-icons/io'; // Icon for the collapse button
import '../styles/FileExplorer.css'; // Import the CSS file

const FileExplorer = ({ isVisible, files, addFile, addFolder, toggleFiles }) => {
  return (
    <div className={`file-explorer ${isVisible ? 'visible' : ''}`}>
      {/* Collapse button */}
      <button className="collapse-button" onClick={toggleFiles}>
        <IoIosArrowBack />
      </button>

      <div className="file-explorer-header">
        <h3>File Explorer</h3>
        <button onClick={addFile}>Add File</button>
        <button onClick={addFolder}>Add Folder</button>
      </div>
      <div className="file-explorer-content">
        {files.length === 0 ? (
          <p>No files or folders available</p>
        ) : (
          <ul>
            {files.map((file, index) => (
              <li key={index}>
                {file.type === 'folder' ? <FaFolder size={20} /> : <FaFile size={20} />}
                {file.name}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default FileExplorer;
