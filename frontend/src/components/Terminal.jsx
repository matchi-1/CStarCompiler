import React from 'react';
import '../styles/Terminal.css';

const Terminal = ({ logs }) => {
  return (
    <div className="terminal">
      <div className="tab-containers">
        <div className="tab-item">
            <p>compiler logs</p>
        </div>
        <div className="tab-filler"></div>
      </div>
      <div className="terminal-body">
        <div className = "table-container">
        <table>
          <tbody>
            {logs.map((log, index) => (
              <tr key={index}>
                <td>{log}</td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      </div>
    </div>
  );
};

export default Terminal;
