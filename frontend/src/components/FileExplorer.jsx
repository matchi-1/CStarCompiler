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
        <p>EXPLORER</p>
        <p>X</p>
      </div>
      <div className="files-menu-container">
        <p>Your Files</p>
        <div className="files-menu-btns-containter">
          <img src="/assets/upload.png" alt="Upload Files" />
          <img src="/assets/new-document.png" alt="New Document" />
          <img src="/assets/new-folder.png" alt="New Folder" />
          <img src="/assets/refresh.png" alt="Refresh" />
        </div>
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
