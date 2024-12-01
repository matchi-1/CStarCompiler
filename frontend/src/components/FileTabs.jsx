import React from 'react';
import '../styles/FileTabs.css';

const FileTabs = ({ openTabs, setOpenTabs, activeTab, setActiveTab, fileData, setFileData  }) => {
  const closeTab = (tabToClose) => {
    setOpenTabs(openTabs.filter((tab) => tab !== tabToClose));
    if (activeTab === tabToClose) {
      setActiveTab(openTabs[0] || null); // Set a new active tab or null if none left
    }
  };

  return (
    <div className="file-tab-containers">
      {openTabs.map((tab, index) => (
        <div
          key={index}
          className={`file-tab-item ${tab === activeTab ? 'file-selected-tab-item' : 'file-unselected-tab-item'}`}
          onClick={() => setActiveTab(tab)}
        >
          <p>{tab}</p>
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