import React from 'react';
import '../styles/FileTabs.css';

const FileTabs = ({  }) => {
  return (
    <div className="file-tab-containers">
        <div className="file-selected-tab-item">
            <p>main.cstar</p>
            <p>x</p>
        </div>
        <div className="file-unselected-tab-item">
            <p>prog1ssdadsadsadasdsadasdsadsa.cstar</p>
            <p>x</p>
        </div>
        <div className="file-unselected-tab-item">
            <p>prog2.cstar</p>
            <p>x</p>
        </div>
        <div className="file-tab-filler"></div>
    </div>
  );
};

export default FileTabs;




