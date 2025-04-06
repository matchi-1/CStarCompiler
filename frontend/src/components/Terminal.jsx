import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import '../styles/Terminal.css';

const socket = io("http://localhost:5000");

const Terminal = ({ logs: initialLogs = [] }) => {
    const terminalRef = useRef();
    const [inputText, setInputText] = useState('');
    const [logs, setLogs] = useState(initialLogs);

    // auto-scroll to bottom on update
    useEffect(() => {
        terminalRef.current?.scrollTo(0, terminalRef.current.scrollHeight);
    }, [logs]);

    // push initial logs (this would be errors from lexer, parser, seman)
    useEffect(() => {
        if (initialLogs.length > 0) {
            setLogs(initialLogs);
        }
    }, [initialLogs]);

    // socket setup
    useEffect(() => {
        const handlePrintOutput = (data) => {
            setLogs(prev => [...prev, { type: 'output', value: data.value }]);
        };

        const handleRequestInput = (data) => {
            setLogs(prev => [...prev, { type: 'input_request', prompt: data.prompt }]);
        };

        const handleError = (data) => {
            setLogs(prev => [...prev, { type: 'error', value: data.message }]);
        };

        const handleDone = () => {
            setLogs(prev => [...prev, { type: 'output', value: "[Loop Finished]" }]);
        };

        socket.on("print_output", handlePrintOutput);
        socket.on("request_input", handleRequestInput);
        socket.on("error", handleError); // TODO: setup socket for runtime errors too
        socket.on("done", handleDone);

        return () => {
            socket.off("print_output", handlePrintOutput);
            socket.off("request_input", handleRequestInput);
            socket.off("error", handleError);
            socket.off("done", handleDone);
        };
    }, []);

    const handleUserInput = (userInput) => {
        setLogs(prevLogs => {
            const updatedLogs = [...prevLogs];
            const lastIndex = updatedLogs.length - 1;

            if (updatedLogs[lastIndex]?.type === 'input_request') {
                const prompt = updatedLogs[lastIndex].prompt;
                updatedLogs[lastIndex] = {
                    type: 'output',
                    value: `${prompt} ${userInput}`
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
                                                    }
                                                }}
                                            />
                                        </div>
                                    </>
                                ) : (
                                    <span>
                                        {log.type === 'error' && <span className="error-marker">|ERROR|</span>}
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
