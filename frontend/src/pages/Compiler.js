import React, { useEffect, useRef, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import FileTabs from '../components/FileTabs';
import FileExplorer from '../components/FileExplorer';
import AnalyzerSegment from '../components/AnalyzerSegment';
import MonacoEditor from '@monaco-editor/react';
import Terminal from '../components/Terminal';
import '../styles/Compiler.css';

const CompilerPage = () => {
  const [openTabs, setOpenTabs] = useState([]);
  const [activeTab, setActiveTab] = useState(null);
  const [fileData, setFileData] = useState([]);

  const editorRef = useRef();
  const editorContainerRef = useRef();
  const resizeObserver = useRef();
  const [code, setValue] = useState('');
  const [output, setOutput] = useState('');
  const [isFilesVisible, setIsFilesVisible] = useState(false); 
  const [lexerResults, setLexerResults] = useState([]);
  const [tokens, setTokens] = useState([]);
  const [errorLogs, setErrors] = useState([]);



  const toggleFiles = () => {
    setIsFilesVisible(!isFilesVisible); // Toggle visibility of the File Explorer
  };


  const onMount = (editor, monaco) => {
    editorRef.current = editor;
    editor.focus();

    if (editorContainerRef.current) {
      resizeObserver.current = new ResizeObserver(() => {
        editor.layout(); // Trigger layout update
      });
      resizeObserver.current.observe(editorContainerRef.current);
    }
  
    // MONACO CUSTOM BLUE THEME (TEST -- WE NEED TO REGISTER OUR PL FIRST B4 WE CAN CUSTOMIZE THIS SATIN)
    const blueTheme = {
      base: 'vs-dark', 
      inherit: true,
      rules: [
        { token: '', background: '181F39', foreground: 'A1ADD5' },
        { token: 'comment', foreground: '5C6370', fontStyle: 'italic' },
        { token: 'keyword', foreground: '569CD6' },
        { token: 'number', foreground: 'B5CEA8' },
        { token: 'string', foreground: 'D69D85' },
        { token: 'variable', foreground: '9CDCFE' },
      ],
      colors: {
        'editor.background': '#181F39',
        'editor.foreground': '#A1ADD5',
        'editorLineNumber.foreground': '#858585',
        'editorCursor.foreground': '#A7A7A7',
      },
    };
  
    monaco.editor.defineTheme('blue-theme', blueTheme);
    monaco.editor.setTheme('blue-theme'); // Apply the theme
  };

  useEffect(() => {
    const fetchTokens = async () => {
      const params = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      };
      const response = await fetch('http://127.0.0.1:5000/api/compile', params);
      const data = await response.json();
      setTokens(data[0]);
      setErrors(data[1]);
    };

    const fetchTimer = setTimeout(fetchTokens, 50);
    return () => clearTimeout(fetchTimer);
  }, [code]);

  // Cleanup ResizeObserver on unmount
  useEffect(() => {
    return () => {
      if (resizeObserver.current) {
        resizeObserver.current.disconnect();
      }
    };
  }, []);

  return (
    <div className="compiler-page">
      <div className="sidebar-container">
        <Sidebar toggleFiles={toggleFiles} /> {/* Pass toggle function to Sidebar */}

        <FileExplorer 
        isVisible={isFilesVisible} toggleFiles={toggleFiles} 
        fileData = {fileData}
        setFileData = {setFileData}
        openTabs={openTabs} 
        setOpenTabs={setOpenTabs} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        />
      </div>

      <div className="compiler-main-container">
        <Header editorRef={editorRef} />
        <FileTabs 
        openTabs={openTabs} 
        setOpenTabs={setOpenTabs} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        fileData={fileData}
        setFileData = {setFileData}
        />

        <div
          className="compiler-content"
          ref={editorContainerRef} // Attach ref to the editor container
        >
         
          <MonacoEditor
            height="100%"
            language="javascript"
            value={code}
            onChange={(value) => setValue(value)}
            onMount={onMount}
            options={{
              automaticLayout: false,
              selectOnLineNumbers: true,
              minimap: {
                enabled: false,
              },
            }}
          />
        </div>
        <Terminal logs={errorLogs} />
      </div>

      <div className="right-segment">
        <AnalyzerSegment tokens={tokens} />
      </div>
    </div>
  );
};

export default CompilerPage;
