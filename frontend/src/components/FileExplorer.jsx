import React, { useState, useRef, useEffect, useMemo } from 'react';
import { FaFolder, FaEdit, FaTrash } from 'react-icons/fa';
import '../styles/FileExplorer.css';
import { db, getDocs, collection } from '../firebaseConfig';
import { doc, updateDoc, addDoc, deleteDoc, query, where } from 'firebase/firestore';


const FileExplorer = ({ isVisible, toggleFiles, openTabs, setOpenTabs, activeTab, setActiveTab
  , fileData, fetchFiles, 
}) => {


  const [hoveredIndex, setHoveredIndex] = useState(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleRefresh = () => {
    fetchFiles();
  };

  const handleUpload = () => {
    fileInputRef.current.click();
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

        newFileName = `${baseName}(${counter})${extension}`;
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

  const handleNewFile = async() => {
    const newFileName = prompt('Enter Cstar source code name: ');
    if (!newFileName) {
      alert('File name cannot be empty.');
      return;
    }
    const filesCollectionRef = collection(db, 'files');
    await addDoc(filesCollectionRef, {
      name: newFileName + ".cstr",
      content: "",
      type: 'file',
      createdAt: new Date(),
    });

    fetchFiles();
  };


  const handleRename = async (file) => {
    let newName = prompt('Enter new name:', file.name);

    if (newName) {
      newName = newName.trim();

      if (file.type == 'file') {
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
    return fileData
      .filter(f => typeof f.name === 'string')
      .slice()
      .sort((a, b) => {
        if (a.type === b.type) {
          return a.name.localeCompare(b.name);
        }
        return a.type === 'folder' ? -1 : 1;
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
            title="Upload Files"
            onClick={handleUpload}
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
            title="New File"
            onClick={handleNewFile}
          />
          <img
            src="/assets/refresh.png"
            alt="Refresh"
            title="Refresh"
            onClick={handleRefresh}
          />

        </div>
      </div>


      <div className='file-explorer-content-wrapper'>
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


    </div>
  );
};

export default FileExplorer;
