import React from 'react';
import { useState } from 'react';
import Editor from '@monaco-editor/react';

function App() {
  const [code, setCode] = useState('// Write your code here!');

  const handleEditorChange = (value) => {
    setCode(value);

  };

  return (
    <div style={{ height: '100vh' }}>
      <Editor
        height="90vh"
        defaultLanguage="javascript"
        defaultValue="// Write your code here!"
        onChange={handleEditorChange}
      />
    </div>
  );
}

export default App;
