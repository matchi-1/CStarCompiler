import React, { useState, useRef, useEffect, useMemo } from 'react';
import { FaFolder, FaFile, FaEdit, FaTrash } from 'react-icons/fa';
import { IoIosArrowBack } from 'react-icons/io'; 
import '../styles/FileExplorer.css';
import { db, getDocs, collection } from '../firebaseConfig';  
import { doc, updateDoc, setDoc,addDoc, deleteDoc, query, where } from 'firebase/firestore';  


const FileExplorer = ({ isVisible, toggleFiles, openTabs, setOpenTabs, activeTab, setActiveTab
   , fileData, setFileData 
}) => {

  const [files, setFiles] = useState([]); 
  
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const fileInputRef = useRef(null); 

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleRefresh = () => {
    fetchFiles(); 
  };
  
  const handleAddFileClick = () => {
      fileInputRef.current.click(); 
    };

  const addFile = (newFile) => {
    setFiles((prevFiles) => [...prevFiles, newFile]); 
  };

  const handleFileClick = (file) => {
    fetchFiles();
  
    if (file.type === "file") {
      // Check if a file with the same name and type already exists in openTabs
      const isFileOpen = openTabs.some(openFile => openFile.name === file.name && openFile.type === file.type);
  
      if (!isFileOpen) {
        setOpenTabs([...openTabs, file]);
      }
  
      setActiveTab(file.name); // Use the file name or unique ID as the activeTab

    }
  };

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

  const handleRename = async (file) => {
    let newName = prompt('Enter new name:', file.name);

    if (newName) {
      newName = newName.trim();

      if(file.type == 'file')
        {
            if (!newName.endsWith('.cstr')) {
              console.log("appended");
            newName += '.cstr';
          }
        }

        if (newName === file.name) {
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
      console.log("active:", activeTab);
      if (activeTab === file.name) {
        console.log(activeTab.name); // This should now print
        setActiveTab(newName);
      }
      setOpenTabs((prevTabs) =>
        prevTabs.map((tab) =>
          tab.id === file.id ? { ...tab, name: newName } : tab
        )
      );

      // Rename in Firestore
      const fileRef = doc(db, 'files', file.id);
      const oldName = file.name;
      await updateDoc(fileRef, { name: newName });

    } catch (error) {
      console.error('Error renaming file in Firestore:', error);
      alert('Failed to rename file in Firestore.');
    }
  }
  fetchFiles();
};

  const handleDelete = async (file) => {
    
    if (window.confirm(`Are you sure you want to delete "${file.name}"?`)) {
      try {
        const fileRef = doc(db, "files", file.id); 
        
        await deleteDoc(fileRef);
  
        // Remove the file from openTabs
      setOpenTabs((prevTabs) =>
        prevTabs.filter((tab) => tab.id !== file.id) // Filter out the deleted file
      );

      // If the deleted file was the active tab, set the active tab to null or the first tab
      if (activeTab === file.name) {
        setActiveTab(openTabs[0].name);  
      }

      fetchFiles(); 

      } catch (error) {
        console.error("Error deleting file from Firestore:", error);
        alert("There was an error deleting the file.");
      }
    }
  };

// Memoize the sorted file data to avoid sorting on each render
const sortedFileData = useMemo(() => {
  return fileData.slice().sort((a, b) => {
    console.log("SUADHIAUSDHIASD");
    if (a.type === b.type) {
      return a.name.localeCompare(b.name); // Alphabetical within type
    }
    return a.type === 'folder' ? -1 : 1; // Folders first
  });
}, [fileData]);

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

      - add dowload button ✅
      

       (folder stuff)
         -add dropdown icon for folders
         -Make folder collapsible.
         -select and deselect folders
         -upload only on specific folders when selected
      */}

      <div className="file-explorer-content">
      {sortedFileData.length === 0 ? (
        <p>No files or folders available</p>
      ) : (
        <ul>
          {sortedFileData.map((file, index) => (
            <li
                key={index}
                onMouseEnter={() => setHoveredIndex(index)} // Set hovered index
                onMouseLeave={() => setHoveredIndex(null)} // Clear hovered index
                onClick={() => handleFileClick(file)} // Add click handler
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
                      onClick={() => handleRename(file)} 
                      title="Edit" 
                    />
                    <FaTrash 
                      className="file-action-icon" 
                      onClick={() => handleDelete(file)} 
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
