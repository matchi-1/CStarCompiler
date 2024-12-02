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
        <Header editorRef={editorRef} />
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
