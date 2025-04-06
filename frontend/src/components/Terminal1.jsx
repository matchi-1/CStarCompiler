// SAMPLE TERMINAL LIKE OUTPUT FOR THE FRONTEND using websocket
import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const socket = io("http://localhost:5000");

function App() {
  const [log, setLog] = useState([]);
  const [currentPrompt, setCurrentPrompt] = useState("");
  const [userInput, setUserInput] = useState("");

  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("print_output", (data) => {
      setLog((prev) => [...prev, data.text]);
    });

    socket.on("request_input", (data) => {
      setCurrentPrompt(data.prompt);
      setLog((prev) => [...prev, data.prompt]);
    });

    socket.on("done", () => {
      setLog((prev) => [...prev, "[Loop Finished]"]);
    });

    return () => {
      socket.off("print_output");
      socket.off("request_input");
      socket.off("done");
    };
  }, []);

  const handleSubmit = () => {
    socket.emit("user_response", { response: userInput });
    setUserInput("");
    setCurrentPrompt("");
  };

  return (
    <div style={{ padding: 20, fontFamily: "monospace", backgroundColor: "#111", color: "#0f0", height: "100vh" }}>
      <div style={{ whiteSpace: "pre-line" }}>
        {log.map((line, idx) => (
          <div key={idx}>{line}</div>
        ))}
      </div>

      {currentPrompt && (
        <div style={{ marginTop: 10 }}>
          <input
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            style={{ backgroundColor: "#222", color: "#0f0", border: "none", padding: "5px", marginRight: "5px" }}
          />
          <button onClick={handleSubmit} style={{ padding: "5px" }}>Send</button>
        </div>
      )}
    </div>
  );
}

export default App;
