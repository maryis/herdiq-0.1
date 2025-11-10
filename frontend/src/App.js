import React, { useState } from "react";

function App() {
  const [response, setResponse] = useState("");

  const callBackend = async () => {
    const res = await fetch("/api/hello");
    const data = await res.json();
    setResponse(data.message);
  };

  const callAgent = async () => {
    const res = await fetch("/agent/ask?query=Hello%20AI");
    const data = await res.json();
    setResponse(data.answer);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>🚀 AI Startup Demo</h1>
      <button onClick={callBackend}>Ping Backend</button>
      <button onClick={callAgent}>Ask Agent</button>
      <p>Response: {response}</p>
    </div>
  );
}

export default App;
