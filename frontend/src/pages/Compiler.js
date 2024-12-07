import React, { useEffect, useRef, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import FileTabs from '../components/FileTabs';
import FileExplorer from '../components/FileExplorer';
import AnalyzerSegment from '../components/AnalyzerSegment';
import MonacoEditor from '@monaco-editor/react';
import Terminal from '../components/Terminal';
import '../styles/Compiler.css';
import { db, getDocs, collection } from '../firebaseConfig';  
import { doc, updateDoc, setDoc,addDoc, deleteDoc, query, where } from 'firebase/firestore';  


{/* 
  TODO: 
  1) add logic for when "hello world.cstr" gets deleted
  
  */}


const CompilerPage = () => {

  const [files, setFiles] = useState([]); 
  const [openTabs, setOpenTabs] = useState([]);
  const [activeTab, setActiveTab] = useState('Hello World.cstr');
  const [fileData, setFileData] = useState([]);
  const resizeObserver = useRef();
  const [code, setValue] = useState();
  const [output, setOutput] = useState('');
  const [isFilesVisible, setIsFilesVisible] = useState(true); 
  const [lexerResults, setLexerResults] = useState([]);
  const [tokens, setTokens] = useState([]);
  const [errorLogs, setErrors] = useState([]);
  const editorRef = useRef();
  const editorContainerRef = useRef();

  useEffect(() => {     //search for Hello world.cstr then set it as active initial tab
    const fetchData = async () => {
      await fetchOrCreateFile(); 
    };
  
    fetchData();
  }, []);

  useEffect(() => {
    if (openTabs.length > 0 && openTabs[0].content) {
      setValue(openTabs[0].content);
    }
  }, [openTabs]);


const fetchOrCreateFile = async () => {     //add TODO item 1 here
  const filesCollectionRef = collection(db, 'files');

  try { // UNCOMMENT EVERYTHING HERE IF "HELLO WORLD.CSTR" IS DELETED 
    const q = query(filesCollectionRef, where('name', '==', 'Hello World.cstr'));
    const querySnapshot = await getDocs(q);
    //  if (!querySnapshot.empty) {
      const fileData = querySnapshot.docs[0].data();
      setOpenTabs([{ id: querySnapshot.docs[0].id, ...fileData }]);
//     } else {
//       const newFileData = {
//         content: `import<iostar> 
//int main(){ 
//  print("Hello World!"); 
//  return 0; 
//}
// // DO NOT DELETE THIS FILE PLEASE FR!!!!!!!!
//         `,
//          name: 'Hello World.cstr',
//          type: 'file',
//        };
//        const docRef = await addDoc(filesCollectionRef, newFileData);
//        setOpenTabs([{ id: docRef.id, ...newFileData }]);
//        console.log('File created with ID:', docRef.id);
//      }
  } catch (error) {
    console.error('Error fetching or creating file:', error);
  }
};

const fetchFiles = async () => {
  try {
    const filesCollectionRef = collection(db, 'files');
    const filesSnapshot = await getDocs(filesCollectionRef);
    const filesList = filesSnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }));

    setFileData(filesList);
  } catch (error) {
    console.error('Error fetching files: ', error);
  }
};

const toggleFiles = () => {
  //setIsFilesVisible(!isFilesVisible); // Toggle visibility of the File Explorer
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
        { token: 'keyword', foreground: '76A1E8'}
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
    console.log("monaco mounted");
    monaco.languages.register({id: 'Cstar'});
    monaco.languages.setMonarchTokensProvider('Cstar', {
      tokenizer: {
        root: [
          [/(\W)\b\d+(\.\d+)?\b/, 'number'],
          [/".*?"/, 'string'],
          [/(\/\/[^\n]*)/, 'comment'],
          [/(\/\*[\s\S]*?\*\/)/, 'comment'],
        ]
      },
    });
    monaco.languages.setLanguageConfiguration('Cstar', {
      autoClosingPairs: [
        { open: '(', close: ')'},
        { open: '{', close: '}'},
        { open: '[', close: ']'},
        { open: '<', close: '>'},
        { open: '"', close: '"'},
        { open: '\'', close: '\''}
      ]
    })
    monaco.languages.registerCompletionItemProvider('Cstar', {
      provideCompletionItems: (model, position) => {
        const currWord = model.getWordUntilPosition(position);
        const wordRange = {
          startLineNumber: position.lineNumber,
          endLineNumber: position.lineNumber,
          startColumn: currWord.startColumn,
          endColumn: currWord.endColumn
        };
        const suggestions = [
          {
            label: 'bool',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'bool',
            range: wordRange
          },
          {
            label: 'break',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'break',
            range: wordRange
          },
          {
            label: 'case',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'case ',
            range: wordRange
          },{
            label: 'char',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'char',
            range: wordRange
          },
          {
            label: 'class',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'class',
            range: wordRange
          },
          {
            label: 'continue',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'continue',
            range: wordRange
          },
          {
            label: 'const',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'const',
            range: wordRange
          },
          {
            label: 'default',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'default',
            range: wordRange
          },
          {
            label: 'do',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'do',
            range: wordRange
          },
          {
            label: 'double',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'double',
            range: wordRange
          },
          {
            label: 'else',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'else',
            range: wordRange
          },
          {
            label: 'false',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'false',
            range: wordRange
          },
          {
            label: 'float',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'float',
            range: wordRange
          },
          {
            label: 'get',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'get',
            range: wordRange
          },
          {
            label: 'if',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'if (${1})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
          {
            label: 'import',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'import',
            range: wordRange
          },
          {
            label: 'in',
            kind:monaco.languages.CompletionItemKind.Function,
            insertText: 'in<${1}>(${2})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
          {
            label: 'int',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'int',
            range: wordRange
          },
          {
            label: 'item',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'item',
            range: wordRange
          },
          {
            label: 'long',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'long',
            range: wordRange
          },
          {
            label: 'print',
            kind:monaco.languages.CompletionItemKind.Function,
            insertText: 'print(${1})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
          {
            label: 'println',
            kind:monaco.languages.CompletionItemKind.Function,
            insertText: 'println(${1})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
          {
            label: 'private',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'private',
            range: wordRange
          },
          {
            label: 'property',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'property',
            range: wordRange
          },
          {
            label: 'repeat',
            kind:monaco.languages.CompletionItemKind.Function,
            insertText: 'repeat (${1})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
          {
            label: 'return',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'return',
            range: wordRange
          },
          {
            label: 'set',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'set',
            range: wordRange
          },
          {
            label: 'static',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'static',
            range: wordRange
          },
          {
            label: 'string',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'string',
            range: wordRange
          },
          {
            label: 'switch',
            kind:monaco.languages.CompletionItemKind.Function,
            insertText: 'switch (${1})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
          {
            label: 'this',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'this',
            range: wordRange
          },
          {
            label: 'true',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'true',
            range: wordRange
          },
          {
            label: 'void',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'void',
            range: wordRange
          },
          {
            label: 'while',
            kind:monaco.languages.CompletionItemKind.Function,
            insertText: 'while (${1})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
        ];
        return {suggestions};
      }
    })
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
        files = {files}
        setFiles = {setFiles}
        openTabs={openTabs} 
        setOpenTabs={setOpenTabs} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        fetchFiles={fetchFiles}

        code={code} 
        setValue={setValue}
        />
      </div>

      <div className="compiler-main-container">
        <Header 
        openTabs={openTabs} 
        setOpenTabs={setOpenTabs} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        fileData={fileData}
        setFileData = {setFileData}
        files = {files}
        setFiles = {setFiles}
        code={code} 
        setValue={setValue}
        editorRef={editorRef} 
        
        />
        <FileTabs 
        openTabs={openTabs} 
        setOpenTabs={setOpenTabs} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        fileData={fileData}
        setFileData = {setFileData}
        files = {files}
        setFiles = {setFiles}
        code={code} 
        setValue={setValue}
        />

        <div
          className="compiler-content"
          ref={editorContainerRef} // Attach ref to the editor container
        >
         
          <MonacoEditor
            height="100%"
            language="Cstar"
            value={code}
            onChange={(value) => setValue(value)}
            onMount={onMount}
            options={{
              automaticLayout: false,
              selectOnLineNumbers: true,
              minimap: {
                enabled: false,
              },
              autoClosingBrackets: true,  // Disable autoClosingBrackets
              autoClosingQuotes: true
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
