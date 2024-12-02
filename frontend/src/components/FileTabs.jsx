import React from 'react';
import '../styles/FileTabs.css';

const FileTabs = ({ openTabs, setOpenTabs, activeTab, setActiveTab, fileData, setFileData  }) => {
  
  const closeTab = (tabToClose) => {
    setOpenTabs(openTabs.filter((tab) => tab !== tabToClose));
    if (activeTab === tabToClose.name) {
      setActiveTab(openTabs[0].name); 
    }
  };

  return (
    <div className="file-tab-containers">
      {openTabs.map((tab, index) => (
        <div
          key={index}
          className={`file-tab-item ${tab.name === activeTab ? 'file-selected-tab-item' : 'file-unselected-tab-item'}`}
          onClick={() => setActiveTab(tab.name)}
        >
          <p>{tab.name}</p>
          <p
            onClick={(e) => {
              e.stopPropagation();
              closeTab(tab);
            }}
          >
            x       {/* put the icon hereee */}
          </p>
        </div>
      ))}
      <div className="file-tab-filler"></div>
    </div>
  );
};

export default FileTabs;