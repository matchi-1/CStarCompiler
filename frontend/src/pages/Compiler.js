import React, { useEffect, useRef, useState } from 'react';
import Sidebar from '../components/Sidebar';
import FileExplorer from '../components/FileExplorer'; 
import TokenTables from '../components/TokenTables';
import MonacoEditor, { loader } from '@monaco-editor/react';
import Terminal from '../components/Terminal';
import '../styles/Compiler.css';

const CompilerPage = () => {
  const editorRef = useRef();
  const [code, setValue] = useState('');
  const [output, setOutput] = useState('');
  const [isFilesVisible, setIsFilesVisible] = useState(false); 
  const [files, setFiles] = useState([]); 
  const [lexerResults, setLexerResults] = useState([])
  const [tokens, setTokens] = useState([])
  const [errorLogs, setErrors] = useState([])

  const onMount = (editor, monaco) => {
    editorRef.current = editor;
    editor.focus();
  
    // MONACO CUSTOM BLUE THEME (TEST -- WE NEED TO REGISTER OUR PL FIRST B4 WE CAN CUSTOMIZE THIS SATIN)
    const blueTheme = {
      base: 'vs-dark', // Base theme (dark mode)
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
  

  const handleCompile = () => {
    const compiledOutput = code.split('').reverse().join('');
    setOutput(compiledOutput);
  };    

  const toggleFiles = () => {
    //setIsFilesVisible(!isFilesVisible); // Toggle visibility when Files button is clicked
  };

  const addFile = () => {
    const newFile = prompt('Enter file name');
    if (newFile) {
      setFiles([...files, { name: newFile, type: 'file' }]);
    }
  };

  const addFolder = () => {
    const newFolder = prompt('Enter folder name');
    if (newFolder) {
      setFiles([...files, { name: newFolder, type: 'folder' }]);
    }
  };

//uesEffects
useEffect(() => {
  const fetchTokens = async() => {
    const params = {
      method:'POST',
      headers: {
          'Content-Type':'application/json' 
      },
      body: JSON.stringify({code})
    };
    var response = await fetch('http://127.0.0.1:5000/api/compile', params);
    var data = await response.json();
    setTokens(data[0]);
    setErrors(data[1]);
  }

  const fetchTimer = setTimeout(fetchTokens, 50);
  return () => clearTimeout(fetchTimer);
}, [code])


  return (
    <div className="compiler-page">
        <div className="sidebar-container">
            <Sidebar toggleFiles={toggleFiles} /> {/* Pass toggle function to Sidebar */}
        </div>
      
      <div className="compiler-main-container">
        {/* Monaco Editor */}
        <div className="compiler-content">
          <MonacoEditor
            height="65%"
            language="javascript"
            value={code}
            onChange={(value) => setValue(value)}
            onMount={onMount}
            options={{
              selectOnLineNumbers: true,
              minimap: {
                enabled: false,
              },
            }}
          />
          <Terminal logs = {errorLogs}/>
        </div>

        {/* Right-side content for file explorer and token tables */}
        <div className="right-segment">
          {/*<FileExplorer 
            isVisible={isFilesVisible} 
            files={files} 
            addFile={addFile} 
            addFolder={addFolder} 
          />*/}
          <TokenTables tokens={tokens}/>
        </div>
      </div>
    </div>
  );
};

export default CompilerPage;
