import React from 'react';
import { FaFolder, FaFile } from 'react-icons/fa';

const darkBlue = "#080e2e";

const FileExplorer = ({ isVisible, files, addFile, addFolder }) => {
  return (
    <div
      className={`file-explorer ${isVisible ? 'visible' : ''}`}
      style={{
        position: 'fixed',
        top: '0',
        left: '0',
        bottom: '0',
        width: '300px', 
        backgroundColor: darkBlue, 
        color: 'white',
        transition: 'transform 0.3s ease',
        transform: isVisible ? 'translateX(0)' : 'translateX(-100%)',
      }}
    >
      <div className="file-explorer-header" style={{ padding: '10px', borderBottom: '1px solid #444' }}>
        <h3>File Explorer</h3>
        <button onClick={addFile}>Add File</button>
        <button onClick={addFolder}>Add Folder</button>
      </div>
      <div className="file-explorer-content" style={{ padding: '10px' }}>
        {files.length === 0 ? (
          <p>No files or folders available</p>
        ) : (
          <ul>
            {files.map((file, index) => (
              <li key={index} style={{ marginBottom: '10px' }}>
                {file.type === 'folder' ? (
                  <FaFolder size={20} />
                ) : (
                  <FaFile size={20} />
                )}
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
