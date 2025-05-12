import React, { useEffect } from 'react';
import '../styles/FileTabs.css';
import { db, getDocs, collection } from '../firebaseConfig';  
import { query, where } from 'firebase/firestore';  

const FileTabs = ({ openTabs, setOpenTabs, activeTab, setActiveTab, setValue
  }) => {
  
  const closeTab = (tabToClose) => {
    setOpenTabs(openTabs.filter((tab) => tab !== tabToClose));
    if (activeTab === tabToClose.name) {
      setActiveTab(openTabs[0].name); 
    }
  };

  useEffect(() => {
    const fetchActiveTabContent = async () => {
      if (!activeTab) return; // Exit if activeTab is not set
  
      try {
        const filesCollectionRef = collection(db, 'files');
        const q = query(filesCollectionRef, where('name', '==', activeTab));
        const querySnapshot = await getDocs(q);
  
        if (!querySnapshot.empty) {
          const fileData = querySnapshot.docs[0].data();
          setValue(fileData.content); // Update the editor's value
        } else {
          console.warn(`File "${activeTab}" not found.`);
          setValue(''); // Clear the editor if no file is found
        }
      } catch (error) {
        console.error('Error fetching file content:', error);
        setValue(''); // Clear the editor on error
      }
    };
  
    fetchActiveTabContent();
  }, [activeTab]);

  const clickTab = (tab) => {
    setActiveTab(tab.name)
  }

  return (
    <div className="file-tab-containers">
      {openTabs.map((tab, index) => (
        <div
          key={index}
          className={`file-tab-item ${tab.name === activeTab ? 'file-selected-tab-item' : 'file-unselected-tab-item'}`}
          onClick={() => clickTab(tab)}
        >
          <div className='file-tab-name'>
            <p>{tab.name}</p>
          </div>
          
          <p
            onClick={(e) => {
              e.stopPropagation();
              closeTab(tab);
            }}
            className='x-tab-btn'
          >
            x      
          </p>
        </div>
      ))}
      <div className="file-tab-filler"></div>
    </div>
  );
};

export default FileTabs;