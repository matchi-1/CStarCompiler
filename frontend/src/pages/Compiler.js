import React, { useEffect, useRef, useState } from 'react';
import Sidebar from '../components/Sidebar';
import FileExplorer from '../components/FileExplorer'; 
import TokenTables from '../components/TokenTables';
import MonacoEditor from '@monaco-editor/react';
import '../styles/Compiler.css';

const CompilerPage = () => {
  const editorRef = useRef();
  const [code, setValue] = useState('');
  const [output, setOutput] = useState('');
  const [isFilesVisible, setIsFilesVisible] = useState(false); 
  const [files, setFiles] = useState([]); 
  const [lexerResults, setLexerResults] = useState([])
  const [tokens, setTokens] = useState([])
  const [errors, setErrors] = useState([])

  const onMount = (editor) => {
    editorRef.current = editor;
    editor.focus();
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
            height="100%" 
            language="javascript" 
            theme="vs-dark"
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

        {/* Right-side content for file explorer and token tables */}
        <div className="right-segment">
          <FileExplorer 
            isVisible={isFilesVisible} 
            files={files} 
            addFile={addFile} 
            addFolder={addFolder} 
          />
          <TokenTables tokens={tokens} errors={errors}/>
        </div>
      </div>
    </div>
  );
};

export default CompilerPage;
