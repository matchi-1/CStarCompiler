import React, { useRef, useState } from 'react';
import { FaFolder, FaFile } from 'react-icons/fa';
import { IoIosArrowBack } from 'react-icons/io'; 
import { initializeApp } from 'firebase/app';
import { getStorage } from 'firebase/storage';
import { getDatabase } from 'firebase/database';
import '../styles/FileExplorer.css'; 

const FileExplorer = ({ isVisible, files, addFolder, toggleFiles, handleFileUpload }) => {
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null); 
  const handleAddFileClick = () => {
      fileInputRef.current.click(); 
    };

  return (
    <div className={`file-explorer ${isVisible ? 'visible' : ''}`}>
      <button className="collapse-button" onClick={toggleFiles}>
        <IoIosArrowBack />
      </button>

      <div className="file-explorer-header">
        <h3>File Explorer</h3>
       
        <button onClick={handleAddFileClick}>Add File</button>
        <button onClick={addFolder}>Add Folder</button>
      </div>


      <div className="file-upload">
        <input
          ref={fileInputRef}  
          type="file"
          accept=".cstr"  
          onChange={handleFileUpload}  
          style={{ display: 'none' }}  
        />
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
