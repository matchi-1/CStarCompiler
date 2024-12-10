import React from 'react';
import '../styles/Header.css';
import { db, getDocs, collection } from '../firebaseConfig';  
import { doc, updateDoc, setDoc,addDoc, deleteDoc, query, where } from 'firebase/firestore';  


const Header = ({ editorRef, fileData, activeTab }) => {
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

  const handleSave = async() => {
    try {
      // Find the document where `name` matches the fileName
      const q = query(collection(db, 'files'), where('name', '==', activeTab));
      const querySnapshot = await getDocs(q);
  
      if (querySnapshot.empty) {
        console.error(`No file found with name: ${activeTab}`);
        return;
      }
  
      // Update the first matching document
      const fileDoc = querySnapshot.docs[0];
      await updateDoc(fileDoc.ref, { 
        content: JSON.parse(localStorage.getItem(activeTab)) });
  
      alert(`${activeTab} content saved successfully!`);
      localStorage.removeItem(activeTab);
    } catch (error) {
      console.error('Error updating content:', error);
    }


    
  }

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
  );
};

export default Header;
