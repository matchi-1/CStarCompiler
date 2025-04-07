import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import '../styles/Terminal.css';

const socket = io("http://localhost:5000");

const Terminal = ({ logs: initialLogs = [], clearLogs, onExecutionComplete }) => {
    const terminalRef = useRef();
    const [inputText, setInputText] = useState('');
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        if (clearLogs) {
            setLogs([]);
        }
    }, [clearLogs]);

    // scroll on log update
    useEffect(() => {
        terminalRef.current?.scrollTo(0, terminalRef.current.scrollHeight);
    }, [logs]);

    // effect for handling changes in initialLogs
    useEffect(() => {
        console.log("initialLogs:", initialLogs);
        if (initialLogs.length > 0) {
            setLogs(initialLogs);
        }
        console.log("all logs:", logs);
    }, [initialLogs]);

    // socket listeners
    useEffect(() => {

        const connectHandler = () => {
            console.log('Connected to backend!');
        };

        const handlePrintOutput = (data) => {
            console.log("Received output string to be displayed:", data);
            setLogs(prev => [...prev, { type: 'output', value: data.value }]);
        };

        const handleRequestInput = (data) => {
            console.log("Received input request:", data);
            setLogs(prev => [...prev, { type: 'input_request', prompt: data.prompt }]);
        };

        const handleError = (data) => {
            setLogs(prev => [...prev, { type: 'error', value: data.message }]);
        };

        const handleDone = (data) => {
            setLogs(prev => [...prev, { type: 'output', value: data.value }]);
            if (onExecutionComplete) {
                onExecutionComplete(); // notify parent that execution is done
            }
        };

        socket.on('connect', connectHandler);
        socket.on('request_input', handleRequestInput);
        socket.on('print_output', handlePrintOutput);
        socket.on('done', handleDone);
        socket.on('error', handleError);

        return () => {
            socket.off('connect', connectHandler);
            socket.off('request_input', handleRequestInput);
            socket.off('print_output', handlePrintOutput);
            socket.off('done', handleDone);
            socket.off('error', handleError);
        };

    }, []);

    const handleUserInput = (userInput) => {
        console.log("Emitting user response:", userInput);

        setLogs(prevLogs => {
            const updatedLogs = [...prevLogs];
            const lastIndex = updatedLogs.length - 1;

            if (updatedLogs[lastIndex]?.type === 'input_request') {
                const prompt = updatedLogs[lastIndex].prompt;

                updatedLogs[lastIndex] = {
                    type: 'output',
                    value: `${prompt}`
                };

                updatedLogs.push({
                    type: 'user_input',
                    value: userInput,
                });
            }

            return updatedLogs;
        });

        socket.emit("user_response", { response: userInput });
        setInputText('');
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
                        {logs && Array.isArray(logs) && logs.map((log, index) => (
                            <div key={index} className={`terminal-line ${log.type}`} style={{ display: 'inline-block' }}>
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
                                                    }
                                                }}
                                            />
                                        </div>
                                    </>
                                ) : log.type === 'user_input' ? (
                                    <span className="user-input-text">{log.value}</span>
                                ) : (
                                    <span>
                                        {log.type === 'error' && <span className="error-marker">|ERROR| </span>}
                                        {log.value ? log.value : log}  {/* value only exists in non-analysis errors */}
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
