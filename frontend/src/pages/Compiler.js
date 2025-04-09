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
  const [isFilesVisible, setIsFilesVisible] = useState(false); 
  const [lexerResults, setLexerResults] = useState([]);
  const [tokens, setTokens] = useState([]);
  const [errorLogs, setErrors] = useState([]);
  const editorRef = useRef();
  const editorContainerRef = useRef();
  const [logs, setLogs] = useState([]);
  const [clearLogs, setClearLogs] = useState(false);

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
      // if (!querySnapshot.empty) {
      const fileData = querySnapshot.docs[0].data();
      setOpenTabs([{ id: querySnapshot.docs[0].id, ...fileData }]);
//       } else {
//         const newFileData = {
//           content: `import<iostar.cstr>; 
// void main(){ 
//   print("Hello World!"); 
//   return; 
// }
// // DO NOT DELETE THIS FILE PLEASE FR!!!!!!!!
        
//           `,
//           name: 'Hello World.cstr',
//           type: 'file',
//          };
//         const docRef = await addDoc(filesCollectionRef, newFileData);
//         setOpenTabs([{ id: docRef.id, ...newFileData }]);
//         console.log('File created with ID:', docRef.id);
//       }
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
  setIsFilesVisible(!isFilesVisible); // Toggle visibility of the File Explorer
};


  const onMount = (editor, monaco) => {
    editorRef.current = editor;
    editor.focus();
    // console.log("Editor instance:", editor);
    // editor.addCommand(
    //   monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter,
    //   () => {
    //       console.log("Ctrl + Shift + Enter pressed!");
    //       callCompiler(); 
    //   }
    // );

    if (editorContainerRef.current) {
      resizeObserver.current = new ResizeObserver(() => {
          if (editorRef.current) {
              editorRef.current.layout(); // Update layout
          }
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
        { token: 'identifier', foreground: 'ffe6bb' },
        { token: 'number', foreground: 'fda88c' },
        { token: 'string', foreground: 'D69D85' },
        { token: 'variable', foreground: '9CDCFE' },
        { token: 'bool', foreground: 'fda88c'},
        { token: 'control', foreground: '5BAEB7'},
        { token: 'private', foreground: 'F9C5C7'},
        { token: 'const', foreground: 'Ffc697'},
        { token: 'output', foreground: '78AED3'},
        { token: 'input', foreground: '78AED3'},
        { token: 'import', foreground: 'a3d5ff'},
        { token: 'type', foreground: '4FC1FF'},
        { token: 'class', foreground: 'fcadb0'},
        { token: 'return', foreground: 'a3d5ff'},
      ],
      colors: {
        'editor.background': '#181F39',
        'editor.foreground': '#A1ADD5',
        'editorLineNumber.foreground': '#858585',
        'editorCursor.foreground': '#A7A7A7',
      },
    };

    const keywords = [
      "bool",
      "break",
      "case",
      "class",
      "continue",
      "const",
      "default",
      "do",
      "double",
      "else",
      "false",
      "float",
      "if",
      "import",
      "in",
      "int",
      "long",
      "print",
      "println",
      "private",
      "repeat",
      "return",
      "string",
      "switch",
      "true",
      "false",
      "void",
      "while",
    ];
  
    monaco.editor.defineTheme('blue-theme', blueTheme);
    monaco.editor.setTheme('blue-theme'); // Apply the theme
    console.log("monaco mounted");
    monaco.languages.register({id: 'Cstar'});
    monaco.languages.setMonarchTokensProvider('Cstar', {
      keywords,
      tokenizer: {
        root: [
          [
            /@?[a-zA-Z][\w$]*/,
            {
              cases: {
                bool: "type",
                int: "type",
                long: "type",
                float: "type",
                double: "type",
                string: "type",
                void: "type",
                if: "control",
                else: "control",
                return: "return",
                for: "control",
                do: "control",
                while: "control",
                continue: "control",
                break: "control",
                switch: "control",
                case: "control",
                default: "control",
                repeat: "control",
                true: "bool",
                false: "bool",
                const: "const",
                private: "private",
                import: "import",
                print: "output",
                println: "output",
                in: "input",
                class: "class",
                "@keywords": "keyword",
                "@default": "identifier",
              },
            },
          ],
          [/\b\d+(\.\d+)?\b/, 'number'],
          [/".*?"/, 'string'],
          [/(\/\/[^\n]*)/, 'comment'],
          [/(\/\*[\s\S]*?\*\/)/, 'comment'],
          [/\/\*/, 'comment', '@comment']
        ],
        comment: [[/\*\//, 'comment', '@pop'], [/./, 'comment.content']],
      },
    });
    monaco.languages.setLanguageConfiguration('Cstar', {
      autoClosingPairs: [
        { open: '(', close: ')'},
        { open: '{', close: '}'},
        { open: '[', close: ']'},
        //{ open: '<', close: '>'},
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
            insertText: 'break;',
            range: wordRange
          },
          {
            label: 'case',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'case ',
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
            insertText: 'continue;',
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
            insertText: 'default:',
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
            label: 'if',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'if (${1})',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range: wordRange
          },
          {
            label: 'import',
            kind:monaco.languages.CompletionItemKind.Keyword,
            insertText: 'import<${1}>;',
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
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

  const callCompiler = async () => {
    console.log("----------------COMPILER RUN BUTTON CLICKED---------------");
    setErrors([]);
    setClearLogs(true);

    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    };
    const response = await fetch('http://127.0.0.1:5000/api/compile', params);
    const { tokens, errors } = await response.json();  // Destructuring response from backend
    
    console.log("errors: " + errors)
    console.log("clicked run button")

    // // combined logs for terminal
    // const excludedMessages = [
    //   // "Parsing completed successfully. No Syntax Errors found.",
    //   // "Semantic analysis completed successfully. No Semantic Errors found."
    // ];
    
    // const errorLogs = errors
    //   .filter(err => !excludedMessages.includes(err))
    //   .map(err => ({ type: 'error', value: err }));
    // const outputLogs = output.map(out => ({ type: 'output', value: out.replace(/\\n/g, '\n') }));
    
    setLogs(errors);  
    setTokens(tokens);

    if (errors.length > 0) {
      handleExecutionComplete();
    }
  }

  const handleExecutionComplete = () => {
    setClearLogs(false);
    console.log(">>>>> [from compiler.js] PROGRAM STILL RUNNING? " + clearLogs)
  };

  // cleanup ResizeObserver on unmount
  useEffect(() => {
    return () => {
      if (resizeObserver.current) {
        resizeObserver.current.disconnect();
      }
    };
  }, []);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.ctrlKey && event.shiftKey && event.key === 'Enter') {
        event.preventDefault(); // Prevent default action if needed
        callCompiler();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);


  return (
    <div className='page-wrapper'>

    
      <div className="compiler-page">
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
        <div className="editor-wrapper">
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
            clickHandler = {callCompiler}
            onExecutionComplete={handleExecutionComplete}
            clearLogs={clearLogs}
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

          
          <div className="tab-menu-terminal-container">
        
            <div className="monaco-editor-wrapper">
              <div
                className="monaco-editor-container"
                ref={editorContainerRef} 
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
                    autoClosingBrackets: true,  
                    autoClosingQuotes: true
                  }}
                />
              </div>
            </div>
            
          </div>
          <Terminal 
            logs={logs} 
            clearLogs={clearLogs}
            onExecutionComplete={handleExecutionComplete}
          />
        </div>
        <div className="right-segment">
            <AnalyzerSegment tokens={tokens} />
        </div>
      </div>
    </div>
  );
};

export default CompilerPage;
