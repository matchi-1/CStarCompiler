import React, { useState, useRef, useEffect } from 'react';
import { FaFolder, FaFile, FaEdit, FaTrash } from 'react-icons/fa';
import { IoIosArrowBack } from 'react-icons/io'; 
import '../styles/FileExplorer.css';
import { db, getDocs, collection } from '../firebaseConfig';  
import { doc, updateDoc, setDoc,addDoc, deleteDoc, query, where } from 'firebase/firestore';  


const FileExplorer = ({ isVisible, toggleFiles }) => {

  const [files, setFiles] = useState([]); 
  const [fileData, setFileData] = useState([]);
  const [hoveredIndex, setHoveredIndex] = useState(null);

  useEffect(() => {
    fetchFiles();
  }, []); 

  const fetchFiles = async () => {
    try {
      const filesCollectionRef = collection(db, 'files');
      const filesSnapshot = await getDocs(filesCollectionRef);
      const filesList = filesSnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
      }));

      setFileData(filesList);
    } catch (error) {
      console.error('Error fetching files: ', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
  
    if (file && file.name.endsWith('.cstr')) {
      let fileName = file.name;

      const baseName = fileName.slice(0, -5); 
      const extension = '.cstr';
  
      const filesCollectionRef = collection(db, 'files');
  
      let newFileName = fileName;
      let counter = 1;
  
      while (true) {
        const q = query(filesCollectionRef, where('name', '==', newFileName));
        const querySnapshot = await getDocs(q);
  
        if (querySnapshot.empty) {
          break;
        }
  
        newFileName = `${baseName} (${counter})${extension}`;
        counter++;
      }
  
      try {
        const fileContent = await new Promise((resolve, reject) => {
          const reader = new FileReader();
  
          reader.onload = () => resolve(reader.result);
          reader.onerror = (error) => reject(error);
  
          reader.readAsText(file);
        });
  
        await addDoc(filesCollectionRef, {
          name: newFileName,
          content: fileContent,
          type: 'file',
          createdAt: new Date(),
        });


        fetchFiles(); 
        console.log(`File uploaded successfully as ${newFileName}.`);
        event.target.value = null;

      } catch (error) {
        console.error('Error uploading file:', error);
        alert('Failed to upload file.');
      }
    } else {
      alert('Please select a .cstr file only.');
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

  const addFolder = async () => {
    const newFolder = prompt('Enter folder name');
    if (newFolder) {

      const filesCollectionRef = collection(db, 'files');

      // Check for duplicates
      const q = query(filesCollectionRef, where('name', '==', newFolder));
      const querySnapshot = await getDocs(q);
  
      if (!querySnapshot.empty) {
        alert('A folder with this name already exists. Please choose a different name.');
        return;
      }

      try {
        const foldersCollectionRef = collection(db, 'files'); 
        
        // Add folder document to Firestore
        await addDoc(foldersCollectionRef, {
          name: newFolder,
          type: 'folder',
          createdAt: new Date(), 
        });
  
        setFiles((prevFiles) => [
          ...prevFiles,
          { name: newFolder, type: 'folder' }
        ]);

        fetchFiles();
  
        console.log(`Folder '${newFolder}' created successfully.`);
      } catch (error) {
        console.error('Error adding folder to Firestore:', error);
        alert('Failed to create folder.');
      }
    }
  };

  const handleRename = async (index) => {
    let newName = prompt('Enter new name:', fileData[index].name);

  if (newName) {
    newName = newName.trim(); // Trim spaces from the beginning and end

    if(fileData[index].type == 'file')
      {
          if (!newName.endsWith('.cstr')) {
          newName += '.cstr';
        }
      }

      if (newName === fileData[index].name) {
        alert('The file name is unchanged.');
        return;
      }

    const filesCollectionRef = collection(db, 'files');

    // Check for duplicates
    const q = query(filesCollectionRef, where('name', '==', newName));
    const querySnapshot = await getDocs(q);

    if (!querySnapshot.empty) {
      alert('A file with this name already exists. Please choose a different name.');
      return;
    }

    try {
      // Rename in Firestore
      const fileRef = doc(db, 'files', fileData[index].id);
      await updateDoc(fileRef, { name: newName });

      // Update local state
      const updatedFiles = [...fileData];
      updatedFiles[index].name = newName;
      setFileData(updatedFiles);

      console.log(`File renamed to ${newName} in Firestore.`);
    } catch (error) {
      console.error('Error renaming file in Firestore:', error);
      alert('Failed to rename file in Firestore.');
    }
  }
};

  const handleDelete = async (index) => {
    const fileToDelete = fileData[index];
    
    if (window.confirm(`Are you sure you want to delete "${fileToDelete.name}"?`)) {
      try {
        const fileRef = doc(db, "files", fileToDelete.id); 
        
        await deleteDoc(fileRef);
  
        const updatedFiles = fileData.filter((_, i) => i !== index);
        setFileData(updatedFiles);
      } catch (error) {
        console.error("Error deleting file from Firestore:", error);
        alert("There was an error deleting the file.");
      }
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


      {/*   
      TODO:

      - add dowload button
      



       (folder stuff)
         -add dropdown icon for folders
         -Make folder collapsible.
         -select and deselect folders
         -upload only on specific folders when selected
      */}

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
