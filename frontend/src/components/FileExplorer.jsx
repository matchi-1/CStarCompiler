import React from 'react';
import { FaFolder, FaFile } from 'react-icons/fa';
import { IoIosArrowBack } from 'react-icons/io'; 
import '../styles/FileExplorer.css'; 

const FileExplorer = ({ isVisible, files, addFile, addFolder, toggleFiles }) => {
  return (
    <div className={`file-explorer ${isVisible ? 'visible' : ''}`}>
      {/* Collapse button */}
      <button className="collapse-button" onClick={toggleFiles}>
        <IoIosArrowBack />
      </button>

      <div className="file-explorer-header">
        <h3>EXPLORER</h3>
        <h3>X</h3>
      </div>

      <button onClick={addFile}>Add File</button>
      <button onClick={addFolder}>Add Folder</button>
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
