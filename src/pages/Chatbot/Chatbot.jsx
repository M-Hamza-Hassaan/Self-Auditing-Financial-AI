import React, { useState } from "react";
import Quiz from "../Quiz/Quiz";

const Chatbot = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  const handleSend = () => {
    if (!prompt.trim()) return;

    setChatHistory((prev) => [...prev, { sender: "user", text: prompt }]);
    setIsGenerating(true);
    setIsPaused(false);

    setTimeout(() => {
      if (!isPaused) {
        const botResponse = `Chatbot: I received your message - "${prompt}"`;
        setChatHistory((prev) => [...prev, { sender: "bot", text: botResponse }]);
        setIsGenerating(false);
      }
    }, 2000);

    setPrompt("");
  };

  const handleClear = () => {
    setChatHistory([]);
    setPrompt("");
  };

  const handleStop = () => {
    setIsGenerating(false);
  };

  const handlePause = () => {
    setIsPaused(true);
  };

  const handleCancel = () => {
    setIsGenerating(false);
    setPrompt("");
    setChatHistory([]);
  };

  return (
    <div style={styles.container}>
      <aside style={styles.sidebar}>
        <div style={styles.header}>
          <h2>AI Assistant</h2>
        </div>

        <div style={styles.chatWindow}>
          {chatHistory.map((message, index) => (
            <div
              key={index}
              style={
                message.sender === "user"
                  ? styles.userMessage
                  : styles.botMessage
              }
            >
              {message.text}
            </div>
          ))}
        </div>

        <div style={styles.inputSection}>
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            style={styles.input}
            placeholder="Type something..."
          />
          <div style={styles.buttonsContainer}>
            {!isGenerating ? (
              <>
                <button onClick={handleClear} style={styles.button}>
                  Clear
                </button>
                <button onClick={handleSend} style={styles.buttonPrimary}>
                  Send
                </button>
              </>
            ) : (
              <>
                <button onClick={handleStop} style={styles.button}>
                  Stop
                </button>
                <button onClick={handlePause} style={styles.button}>
                  Pause
                </button>
                <button onClick={handleCancel} style={styles.buttonDanger}>
                  Cancel
                </button>
              </>
            )}
          </div>
        </div>
      </aside>

      <main style={styles.mainContent}>
        < Quiz style={styles.mainHeading} />
        <p style={styles.mainText}>
          Use the sidebar to communicate with the chatbot and receive instant responses.
        </p>
      </main>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    height: "100vh",
    backgroundColor: "#f9fafb",
    fontFamily: "'Inter', sans-serif",
  },
  sidebar: {
    width: "400px",
    background: "linear-gradient(135deg, #6EE7B7, #3B82F6)", // Soft green to blue gradient
    color: "#ffffff",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    padding: "20px",
    textAlign: "center",
    borderBottom: "2px solid rgba(255, 255, 255, 0.2)",
  },
  chatWindow: {
    flex: 1,
    overflowY: "auto",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  userMessage: {
    alignSelf: "flex-end",
    background: "#4CAF50", // Softer green for user messages
    color: "#ffffff",
    padding: "12px 16px",
    borderRadius: "20px",
    maxWidth: "75%",
    wordWrap: "break-word",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  botMessage: {
    alignSelf: "flex-start",
    background: "#60A5FA", // Soft blue for bot messages
    color: "#ffffff",
    padding: "12px 16px",
    borderRadius: "20px",
    maxWidth: "75%",
    wordWrap: "break-word",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  inputSection: {
    padding: "20px",
    borderTop: "2px solid rgba(255, 255, 255, 0.2)",
    backgroundColor: "#3B82F6", // Matching blue tone for the input section
  },
  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    marginBottom: "10px",
    fontSize: "16px",
    outline: "none",
    background: "#ffffff",
    color: "#111827",
  },
  buttonsContainer: {
    display: "flex",
    gap: "10px",
  },
  button: {
    flex: 1,
    padding: "10px",
    fontSize: "14px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    backgroundColor: "#64748b",
    color: "#ffffff",
    transition: "transform 0.2s, background-color 0.2s",
  },
  buttonPrimary: {
    flex: 1,
    padding: "10px",
    fontSize: "14px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    backgroundColor: "#34D399", // Soft green for Send button
    color: "#ffffff",
    transition: "transform 0.2s, background-color 0.2s",
  },
  buttonDanger: {
    flex: 1,
    padding: "10px",
    fontSize: "14px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    backgroundColor: "#F87171", // Soft red for Cancel button
    color: "#ffffff",
    transition: "transform 0.2s, background-color 0.2s",
  },
  mainContent: {
    flex: 1,
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
  },
  mainHeading: {
    fontSize: "32px",
    fontWeight: "bold",
    marginBottom: "20px",
    color: "#111827",
  },
  mainText: {
    fontSize: "18px",
    color: "#4b5563",
  },
};

export default Chatbot;
