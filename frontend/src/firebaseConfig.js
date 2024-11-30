import { getFirestore, collection, getDocs } from 'firebase/firestore';
import { getStorage, ref, uploadBytes } from 'firebase/storage';  
import { initializeApp } from 'firebase/app';  


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
  const db = getFirestore(app);

export{db, app, collection, getDocs};