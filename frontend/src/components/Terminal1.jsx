import React, { useState, useEffect, useRef } from 'react';
import '../styles/Terminal.css';

const Terminal = ({ logs = [] }) => {
  const terminalRef = useRef();
  const [inputText, setInputText] = useState('');
  const [logs, setLogs] = useState([]);

  /*// sample logs from backend (replace with socket events later)
  useEffect(() => {
    setLogs([
      { type: 'output', value: 'Hello world!' },
      { type: 'error', value: 'Runtime error on line 2' },
      { type: 'output', value: 'Hello world!' },
      { type: 'input_request', prompt: 'Enter your nameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee:' },
    ]);
  }, []);*/

  const handleUserInput = (userInput) => {
    setLogs((prevLogs) => {
      const updatedLogs = [...prevLogs];
      const lastIndex = updatedLogs.length - 1;

      // if the last log is an input prompt, replace it as an output log -- tho this may change based on backend logic
      if (updatedLogs[lastIndex]?.type === 'input_request') {
        const promptText = updatedLogs[lastIndex].prompt;
        updatedLogs[lastIndex] = {
          type: 'output',
          value: `${promptText} ${userInput}`
        };
      }

      // (optional) Emit to backend here
      // socket.emit("user_input", { value: userInput });

      return updatedLogs;
    });
  };


  return (
    <div className="terminal">
      <div className="tab-containers">
        <div className="tab-item">
          <p>Compiler Logs</p>
        </div>
        <div className="tab-filler">
          <p className="x-tab-btn">x</p>
        </div>
      </div>

      <div className="terminal-body">
        <div className="table-container">
          <div className="table-wrapper">
            <div className="terminal-cont" ref={terminalRef}>
              {logs.map((log, index) => (
                <div key={index} className={`terminal-line ${log.type}`}>
                  {log.type === 'input_request' ? (
                    <>
                      <span className="prompt">{log.prompt}</span>
                      <div className="input-wrapper">
                        <span className="ghost">{inputText || ' '}</span>
                        <input
                          type="text"
                          className="terminal-input"
                          value={inputText}
                          onChange={(e) => setInputText(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                              handleUserInput(inputText);
                              setInputText('');
                            }
                          }}
                        />
                      </div>
                    </>
                  ) : (
                    <span>{log.value}</span>
                  )}
                </div>
              ))}
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default Terminal;
