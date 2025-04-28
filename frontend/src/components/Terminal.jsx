import React, { useState, useEffect, useCallback, useRef } from 'react';
import { io } from 'socket.io-client';
import '../styles/Terminal.css';

const socket = io("http://localhost:5000");
// const socket = io("https://cstar-backend-217043973303.asia-southeast1.run.app", {
//     transports: ["websocket"],
//     secure: true
//   });

const Terminal = ({ logs: initialLogs = [], clearLogs, onExecutionComplete }) => {
    const terminalRef = useRef();
    const [inputText, setInputText] = useState('');
    const [logs, setLogs] = useState([]);
    const logsRef = useRef(logs);
    logsRef.current = logs;

    const formattedInitialLogs = initialLogs.map(log => ({
        type: 'error',
        value: log
    }));


    const parseEscapeSequences = (str, isOutput = false) => {
        let formattedStr = str.replace(/\\t/g, '\t')  // \t to tab
            .replace(/\\"/g, '"')   // \\" to "
            .replace(/\\\\/g, '\\'); // \\ to backslash

        if (!isOutput)
            str.replace(/\\n/g, '\n')

        return formattedStr
    };

    // clear logs when clearLogs prop osci
    useEffect(() => {
        console.log(">>>>> [from terminal.jsx] PROGRAM STILL RUNNING? " + clearLogs)
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
            setLogs(formattedInitialLogs);
        }
        console.log("all logs:", logs);
    }, [initialLogs]);


    // socket handlers
    const connectHandler = () => {
        console.log('Connected to backend!');
    };

    const handlePrintOutput = useCallback((data) => {
        console.log("Received output string to be displayed:", data);

        const value = parseEscapeSequences(data.value.toString(), true); //parseEscapeSequences(data.value.toString());

        // if there's no newline, append directly to the last log
        if (!value.includes('\n')) {
            setLogs(prevLogs => {
                const updatedLogs = [...prevLogs];
                const last = updatedLogs[updatedLogs.length - 1];

                if (last && last.type === 'output') {
                    // replace the last log entry with a new object
                    const newLast = { ...last, value: last.value + value };
                    updatedLogs[updatedLogs.length - 1] = newLast;
                } else {
                    updatedLogs.push({ type: 'output', value });
                }

                return updatedLogs;
            });
            return;
        }

        // else, split and stream line-by-line
        const parts = value.split('\n');

        setLogs(prevLogs => {
            const updatedLogs = [...prevLogs]; // Start with the previous logs

            parts.forEach((part, index) => {
                const isLast = index === parts.length - 1;

                if (isLast) {
                    const last = updatedLogs[updatedLogs.length - 1];
                    if (last && last.type === 'output') {
                        // clone and replace to avoid mutation
                        const newLast = { ...last, value: last.value + part };
                        updatedLogs[updatedLogs.length - 1] = newLast;
                    } else {
                        updatedLogs.push({ type: 'output', value: part });
                    }
                } else {
                    if (part !== '') {
                        const last = updatedLogs[updatedLogs.length - 1];
                        if (last && last.type === 'output') {
                            // clone and replace to avoid mutation
                            const newLast = { ...last, value: last.value + part };
                            updatedLogs[updatedLogs.length - 1] = newLast;
                        } else {
                            updatedLogs.push({ type: 'output', value: part });
                        }
                    }
                    updatedLogs.push({ type: 'output', value: '' }); // newline marker
                }
            });

            // Update the logs state with the updated logs array
            return updatedLogs;
        });

    }, []);

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
        handleUserInput("");
        setLogs(prev => [...prev, { type: 'success', value: data.value.toString() }]);
        if (onExecutionComplete) {
            onExecutionComplete(); // notify parent that execution is done
        }
    };



    // socket listeners
    useEffect(() => {
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
                    {clearLogs && <p>Program running . . .</p>}
                </div>
                {/* <div className="tab-filler">
                    <p className="x-tab-btn">x</p>
                </div> */}

            </div>

            <div className="terminal-body">
                <div className="logs-container">
                    <div className="terminal-cont" ref={terminalRef}>
                        {logs && Array.isArray(logs) && logs.map((log, index) => {
                            return (
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
                                            {log.value}
                                        </span>
                                    )}
                                </div>
                            );
                        })}


                    </div>
                </div>
            </div>
        </div>
    );
};

export default Terminal;
