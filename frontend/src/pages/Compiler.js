import React, { useEffect, useRef, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import FileTabs from '../components/FileTabs';
import FileExplorer from '../components/FileExplorer'; 
import AnalyzerSegment from '../components/AnalyzerSegment';
import MonacoEditor, { loader } from '@monaco-editor/react';
import Terminal from '../components/Terminal';
import { initializeApp } from 'firebase/app';
import { getAnalytics } from "firebase/analytics";
import { getStorage } from 'firebase/storage';
import { getDatabase } from 'firebase/database';
import '../styles/Compiler.css';

const CompilerPage = () => {

  const firebaseConfig = {
    apiKey: "AIzaSyCK3i8_VWMzXV1HQnSANH1K0JEMiuna73U",
    authDomain: "cstar-compiler.firebaseapp.com",
    databaseURL: "https://cstar-compiler-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "cstar-compiler",
    storageBucket: "cstar-compiler.firebasestorage.app",
    messagingSenderId: "893952768568",
    appId: "1:893952768568:web:57f14acf00c05626a584cd",
    measurementId: "G-GYVZ4F33W6"
  };
  
  
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
  
  const storage = getStorage(app);
  const database = getDatabase(app);


  const [uploading, setUploading] = useState(false);
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
    setIsFilesVisible(!isFilesVisible); // Toggle visibility when Files button is clicked
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0]; 
    if (file && file.name.endsWith('.cstr')) {
      const newFile = {
        name: file.name,  
        type: 'file',     
        fileContent: file,
      };
      addFile(newFile); 
    } else {
      alert('Please select a .cstr file only'); 
    }
  };

  const addFile = (newFile) => {
    setFiles((prevFiles) => [...prevFiles, newFile]); // Adds the new file to the state
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
            <FileExplorer 
              isVisible={isFilesVisible} 
              files={files} 
              addFile={addFile} 
              addFolder={addFolder} 
              toggleFiles={toggleFiles} 
               handleFileUpload={handleFileUpload}
            />

        </div>
      
      <div className="compiler-main-container">
        <Header/>
        <FileTabs/>
        
        <div className="compiler-content">
          {/* Monaco Editor */}
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
        </div>
        <Terminal logs = {errorLogs}/>
      </div>
      
      {/* Right-side content for file explorer and token tables */}
      <div className="right-segment">
        <AnalyzerSegment tokens={tokens}/>
      </div>
      
    </div>
  );
};

export default CompilerPage;
