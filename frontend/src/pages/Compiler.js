import React, { useState } from 'react';
import Sidebar from '../components/Sidebar'; 
import '../styles/Compiler.css'; 

const CompilerPage = () => {
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');

  const handleCompile = () => {
    const compiledOutput = code.split('').reverse().join('');
    setOutput(compiledOutput);
  };

  return (
    <div style={{ display: 'flex' }}>
      <Sidebar /> {/* Sidebar */}
      <div style={{ marginLeft: '200px', padding: '20px', flex: 1 }}>
        <h1>Compiler Page</h1>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter code here"
          rows="10"
          style={{ width: '100%', padding: '10px', fontSize: '16px' }}
        />
        <button
          onClick={handleCompile}
          style={{
            marginTop: '10px',
            padding: '10px 20px',
            fontSize: '16px',
            cursor: 'pointer',
          }}
        >
          Compile
        </button>

        <div style={{ marginTop: '20px' }}>
          <h2>Output</h2>
          <pre>{output}</pre>
        </div>
      </div>
    </div>
  );
};

export default CompilerPage;
