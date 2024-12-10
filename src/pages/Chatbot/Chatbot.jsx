import React, { useState } from "react";
import { Button } from "../../components/ui/button"
import { Input } from "../../components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card"
import { X } from 'lucide-react'

const Chatbot = ({ onClose }) => {
  const [chatHistory, setChatHistory] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleSend = async () => {
    if (!prompt.trim()) return;

    setChatHistory((prev) => [...prev, { sender: "user", text: prompt }]);
    setIsGenerating(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.error) {
        throw new Error(data.error);
      }

      setChatHistory((prev) => [...prev, { sender: "bot", text: data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setChatHistory((prev) => [...prev, { sender: "bot", text: `Error: ${error.message}. Please try again.` }]);
    } finally {
      setIsGenerating(false);
      setPrompt("");
    }
  };

  return (
    <Card className="h-full flex flex-col relative">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>AI Assistant</CardTitle>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="h-4 w-4" />
        </Button>
      </CardHeader>
      <CardContent className="flex-grow overflow-auto">
        {chatHistory.map((message, index) => (
          <div
            key={index}
            className={`mb-2 p-2 rounded-lg ${
              message.sender === "user" ? "bg-blue-100 text-right" : "bg-gray-100"
            }`}
          >
            {message.text}
          </div>
        ))}
      </CardContent>
      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <Input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your message..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button onClick={handleSend} disabled={isGenerating}>
            {isGenerating ? "Generating..." : "Send"}
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default Chatbot;

