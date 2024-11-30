import React, { useState, useRef, useEffect } from 'react';
import { FaFolder, FaFile, FaEdit, FaTrash } from 'react-icons/fa';
import { IoIosArrowBack } from 'react-icons/io'; 
import '../styles/FileExplorer.css';
import { db, getDocs, collection } from '../firebaseConfig';  
import { doc, setDoc } from 'firebase/firestore';  


const FileExplorer = ({ isVisible, toggleFiles }) => {

  const [files, setFiles] = useState([]); 
  const [fileData, setFileData] = useState([]);
  const [hoveredIndex, setHoveredIndex] = useState(null);

  useEffect(() => {
    fetchFiles();
  }, []); 

  const fetchFiles = async () => {
    try {
      // Get reference to the 'files' collection
      const filesCollectionRef = collection(db, 'files');
      // Fetch the documents from the collection
      const filesSnapshot = await getDocs(filesCollectionRef);
      // Map through the snapshot to get the data
      const filesList = filesSnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
      }));
      // Set the file data in state
      setFileData(filesList);
    } catch (error) {
      console.error('Error fetching files: ', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
  
    if (file && file.name.endsWith('.cstr')) {
      const reader = new FileReader();
  
      reader.onload = async () => {
        const fileContent = reader.result;
  
        try {
          // Save file data to Firestore
          await setDoc(doc(db, 'files', file.name), {
            name: file.name,
            content: fileContent,
            uploadedAt: new Date().toISOString(),
            size: file.size,
          });
  
            const newFile = {
            name: file.name,
            type: 'file',
            content: fileContent,
          };
  
          addFile(newFile); 
          alert('File uploaded successfully!');
        } catch (error) {
          console.error('Error uploading file to Firestore:', error);
          alert('Failed to upload the file.');
        }
      };
  
      reader.readAsText(file);  
    } else {
      alert('Please select a .cstr file only');
    }
  };

  const handleRefresh = () => {
    fetchFiles(); 
  };

  const fileInputRef = useRef(null); 
  const handleAddFileClick = () => {
      fileInputRef.current.click(); 
    };

  const addFile = (newFile) => {
    setFiles((prevFiles) => [...prevFiles, newFile]); 
  };

  const addFolder = () => {
    const newFolder = prompt('Enter folder name');
    if (newFolder) {
      setFiles([...files, { name: newFolder, type: 'folder' }]);
    }
  };

  const handleRename = (index) => {
    const newName = prompt('Enter new name:', fileData[index].name);
    if (newName && newName !== fileData[index].name) {
      const updatedFiles = [...fileData];
      updatedFiles[index].name = newName;
      setFileData(updatedFiles);
    }
  };

  const handleDelete = (index) => {
    if (window.confirm(`Are you sure you want to delete "${fileData[index].name}"?`)) {
      const updatedFiles = fileData.filter((_, i) => i !== index);
      setFileData(updatedFiles);
    }
  };

  return (
    <div className={`file-explorer ${isVisible ? 'visible' : ''}`}>
      <div className="file-explorer-header">
        <p>EXPLORER</p>
        <p id="explorer-collapse-btn" onClick={toggleFiles}>X</p>
      </div>
      <div className="files-menu-container">
        <p>Your Files</p>
        <div className="files-menu-btns-container">
          <img
            src="/assets/upload.png"
            alt="Upload Files"
            onClick={handleAddFileClick}
          />
        <input
          ref={fileInputRef}  
          type="file"
          accept=".cstr"  
          onChange={handleFileUpload}  
          style={{ display: 'none' }}  
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
            onClick={handleRefresh}
          />

        </div>
      </div>

      <div className="file-explorer-content">
        {fileData.length === 0 ? (
          <p>No files or folders available</p>
        ) : (
          <ul>
            {fileData.map((file, index) => (
              <li
                key={index}
                onMouseEnter={() => setHoveredIndex(index)} // Set hovered index
                onMouseLeave={() => setHoveredIndex(null)} // Clear hovered index
                className="file-item"
              >
                {file.type === 'folder' ? (
                    <FaFolder size={12} />
                  ) : (
                    <img src="/assets/CStarLogo2.png" alt="Cstar" className="CStar-file-icon" />
                  )}
                  <span className="file-name">{file.name}</span>


                {hoveredIndex === index && ( // Show buttons only if this file is hovered
                  <span className="file-actions">
                    <FaEdit 
                      className="file-action-icon" 
                      onClick={() => handleRename(index)} 
                      title="Edit" 
                    />
                    <FaTrash 
                      className="file-action-icon" 
                      onClick={() => handleDelete(index)} 
                      title="Delete" 
                  />
                </span>                
                )}
              </li>
            ))}
          </ul>
        )}
      </div>


    </div>
  );
};

export default FileExplorer;
