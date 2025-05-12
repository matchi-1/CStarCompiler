import React, { useEffect } from 'react';
import '../styles/Header.css';
import { io } from 'socket.io-client';
import { db, getDocs, collection } from '../firebaseConfig';  
import { doc, updateDoc, setDoc,addDoc, deleteDoc, query, where } from 'firebase/firestore';  

const socket = io("http://localhost:5000");
// const socket = io("https://cstar-backend-217043973303.asia-southeast1.run.app", {
//   transports: ["websocket"],
//   secure: true
// });

const Header = ({ editorRef, fileData, activeTab, clickHandler, clearLogs, onExecutionComplete, code, setValue, setFileData }) => {

  const handleTerminate = () => {
    console.log("Terminating program...");
    socket.emit("terminate_runtime");
    onExecutionComplete()
  };


  useEffect(() => {
    console.log(">>>>> [from header.jsx] PROGRAM STILL RUNNING? " + clearLogs)
  }, [clearLogs]);

  // Undo functionality
  const handleUndo = () => {
    if (editorRef.current) {
      editorRef.current.trigger('keyboard', 'undo', null);
    }
  };

  // Redo functionality
  const handleRedo = () => {
    if (editorRef.current) {
      editorRef.current.trigger('keyboard', 'redo', null);
    }
  };

    // Save functionality
    const handleSave = async () => {
      console.log("Saving file...");
      if (!activeTab){ console.log("ACTIVE TAB NOT SETT!!!"); return; }
      
      try {
        const filesCollectionRef = collection(db, 'files');
        const q = query(filesCollectionRef, where('name', '==', activeTab));
        console.log("query: ", q);
        console.log("updatign file with: ", code);
        const querySnapshot = await getDocs(q);
  
        if (!querySnapshot.empty) {
          // const fileData = querySnapshot.docs[0].data();
          await updateDoc(/** @type {DocumentReference} */(querySnapshot.docs[0].ref), {
            content: code
          });
          console.log("File saved successfully!");
          alert("File saved successfully!");
          //setValue(fileData.content); // Update the editor's value
        } else {
          console.warn(`File "${activeTab}" not found.`);
          setValue(''); // Clear the editor if no file is found
        }
      } catch (error) {
        console.error('Error fetching file content:', error);
        setValue(''); // Clear the editor on error
      }
    };
  

  const handleDownload = () => {
    const file = fileData.find((file) => file.name === activeTab);
    if (file) {
      const blob = new Blob([file.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = file.name; // Use file name for the download
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } else {
      alert('No file selected for download.');
    }
  };

  return (
    <div className="header">
      <div className='header-menu'>
        <div className="header-item" onClick={handleUndo}>
          <p>Undo</p>
        </div>
        <div className="header-item" onClick={handleRedo}>
          <p>Redo</p>
        </div>
        <div className="header-item" onClick={handleSave}>
          <p>Save</p>
        </div>
        <div className="header-item" onClick={handleDownload}>
          <p>Download</p>
        </div>
      </div>

      <div className='header-btns'>
        <div className={`img-btn-wrapper ${clearLogs ? 'disabled' : ''}`} onClick={clickHandler}>
          <img src="/assets/run-btn.png" alt="run-btn" />
        </div>

        <div className={`stop-btn-wrapper ${!clearLogs ? 'disabled' : ''}`} onClick={handleTerminate}>
          <img src="/assets/stop-btn.png" alt="stop-btn" />
        </div>
      </div>

    </div>
  );
};

export default Header;
