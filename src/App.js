import React, { useState } from "react";
import Navbar from './pages/Navbar/Navbar';
import Chatbot from './pages/Chatbot/Chatbot';
import './App.css';
import InputSection from "./components/InputSection";
import OutputSection from "./components/OutputSection";
import Refinements from "./components/Refinement";
function App() {
  return (
    <div>
      <Navbar />
      <Chatbot />
    </div>
  );
}


  const [generatedContent, setGeneratedContent] = useState(null);
  const [refinements, setRefinements] = useState(null);

  const handleGenerate = (inputData) => {
    // Simulate API call for content generation
    const mockData = {
      text: "AI trends are reshaping industries globally!",
      image: "https://via.placeholder.com/150",
      video: "https://example.com/mock-video.mp4",
      meme: "https://via.placeholder.com/250?text=Funny+Meme",
    };
    setGeneratedContent(mockData);
  };

  const handleRefinement = (newRefinement) => {
    // Simulate applying refinements
    setRefinements(newRefinement);
  };

  // Apply refinements to the generated content (for example, modifying text)
  const applyRefinement = (content) => {
    if (refinements === "shorten") {
      return { ...content, text: content.text.slice(0, 30) + "..." };
    }
    if (refinements === "changeTone") {
      return { ...content, text: "Exciting AI trends are transforming industries!" };
    }
    return content;
  };

  const refinedContent = generatedContent ? applyRefinement(generatedContent) : null;

  
    <div className="App">
      <h1>AI Content Generator</h1>
      <InputSection onGenerate={handleGenerate} />
      {refinedContent && (
        <>
          <OutputSection content={refinedContent} />
          <Refinements onRefine={handleRefinement} />
        </>
      )}
    </div>
  ;



export default App;
