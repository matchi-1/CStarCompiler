import React, { useState } from 'react';
import { FaFolder, FaFile } from 'react-icons/fa';
import { IoIosArrowBack } from 'react-icons/io'; 
import '../styles/FileExplorer.css';

const FileExplorer = ({ isVisible, toggleFiles }) => {
  const [files, setFiles] = useState([]); // Manage files/folders state locally muna

  const addFile = () => {
    const newFile = prompt('Enter file name');
    if (newFile) {
      setFiles([...files, { name: newFile, type: 'file' }]);
    }
  };

  const addFolder = () => {
    const newFolder = prompt('Enter folder name');
    if (newFolder) {
      setFiles([...files, { name: newFolder, type: 'folder' }]);
    }
  };

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
          <img
            src="/assets/upload.png"
            alt="Upload Files"
            onClick={() => alert('wala pa')}
          />
          <img
            src="/assets/new-document.png"
            alt="New Document"
            onClick={addFile} 
          />
          <img
            src="/assets/new-folder.png"
            alt="New Folder"
            onClick={addFolder} 
          />
          <img
            src="/assets/refresh.png"
            alt="Refresh"
            onClick={() => alert('wala pa')}
          />
        </div>
      </div>
      <div className="file-explorer-content">
        {files.length === 0 ? (
          <p>No files or folders available</p>
        ) : (
          <ul>
            {files.map((file, index) => (
              <li key={index}>
                {file.type === 'folder' ? <FaFolder size={12} /> : <FaFile size={12} />}
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
