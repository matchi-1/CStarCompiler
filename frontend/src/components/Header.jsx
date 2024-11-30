import React from 'react';
import '../styles/Header.css';

const Header = ({  }) => {
  return (
    <div className="header">
        <div className="header-item">
            <p>Save</p>
        </div>
        <div className="header-item">
            <p>Undo</p>
        </div>
        <div className="header-item">
            <p>Redo</p>
        </div>
    </div>
  );
};

export default Header;
