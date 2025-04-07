import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import '../styles/Terminal.css';

const socket = io("http://localhost:5000");

const Terminal = ({ logs: initialLogs = [], clearLogs, onExecutionComplete }) => {
    const terminalRef = useRef();
    const [inputText, setInputText] = useState('');
    const [logs, setLogs] = useState([]);

    const parseEscapeSequences = (str) => {
        return str
            .replace(/\\n/g, '\n')  // \n to newline
            .replace(/\\t/g, '\t')  // \t to tab
            .replace(/\\b/g, '\b')  // \b to backspace
            .replace(/\\"/g, '"')   // \\" to "
            .replace(/\\\\/g, '\\'); // \\ to backslash
    };

    const groupLogsForDisplay = (logs) => {
        const groups = [];
        let currentOutputGroup = '';

        logs.forEach((log) => {
            if (log.type === 'output') {
                currentOutputGroup += parseEscapeSequences(log.value);
            } else {
                groups.push(currentOutputGroup);
                groups.push(log);
                currentOutputGroup = '';
            }
        });

        return groups;
    };

    const groupedLogs = groupLogsForDisplay(logs);

    // clear logs when clearLogs prop osci
    useEffect(() => {
        if (clearLogs) {
            setLogs([]);
        }
    }, [clearLogs]);


    // scroll on log update
    useEffect(() => {
        terminalRef.current?.scrollTo(0, terminalRef.current.scrollHeight);

        console.log("current logs on logs change:", logs);
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
            setLogs(prev => [...prev, { type: 'output', value: data.value.toString() }]);
        };

        const handleRequestInput = (data) => {
            console.log("Received input request:", data);
            setLogs(prev => [...prev, { type: 'input_request', prompt: data.prompt.toString() }]);
        };

        const handleError = (data) => {
            console.log("Received runtime error:", data);
            setLogs(prev => [...prev, { type: 'error', value: data.value.toString() }]);
            if (onExecutionComplete) {
                onExecutionComplete(); // notify parent that execution is done
            }
        };

        const handleDone = (data) => {
            setLogs(prev => [...prev, { type: 'success', value: data.value.toString() }]);
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

                // replace input_request with a user_input type that holds both prompt and value
                updatedLogs[lastIndex] = {
                    type: 'user_input',
                    prompt: prompt,
                    value: userInput,
                };
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
                        {logs && Array.isArray(logs) && groupedLogs.map((log, index) => (
                            <div key={index} className={`terminal-line ${log.type}`} style={{ display: 'block' }}>
                                {log.type === 'input_request' ? (
                                    <>
                                        <span className="prompt">{parseEscapeSequences(log.prompt)}</span>
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
                                    <span className="user-input-text">
                                        <span className="prompt">{parseEscapeSequences(log.prompt)}</span>
                                        {log.value}
                                    </span>
                                ) : (
                                    <span>
                                        {log.type === 'error' && <span className="error-marker">|ERROR| </span>}
                                        {log.value ? log.value : log}
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
