import React, { useState, useEffect, useRef } from 'react';
import '../styles/Terminal.css';

const Terminal = ({ logs: initialLogs = [] }) => {
    const terminalRef = useRef();
    const [inputText, setInputText] = useState('');
    const [internalLogs, setInternalLogs] = useState(initialLogs);

    useEffect(() => {
        setInternalLogs(initialLogs);  // update when parent sends new logs
    }, [initialLogs]);

    const handleUserInput = (userInput) => {
        setInternalLogs((prevLogs) => {
            const updatedLogs = [...prevLogs];
            const lastIndex = updatedLogs.length - 1;

            if (updatedLogs[lastIndex]?.type === 'input_request') {
                const promptText = updatedLogs[lastIndex].prompt;
                updatedLogs[lastIndex] = {
                    type: 'output',
                    value: `${promptText} ${userInput}`
                };
            }

            // send to backend later ?
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
                <div className="logs-container">
                    <div className="terminal-cont" ref={terminalRef}>
                        {internalLogs.map((log, index) => (
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
                                    <span>
                                        {log.type === 'error' && <span className="error-marker">|ERROR|</span>} {/* error messages */}
                                        {log.value}
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Terminal;
