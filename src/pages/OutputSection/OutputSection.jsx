import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

const OutputSection = ({ content }) => {
  return (
    <Card className="output-section">
      <CardHeader>
        <CardTitle>Generated Content</CardTitle>
      </CardHeader>
      <CardContent>
        {content.text && <p className="mb-4 text-lg">{content.text}</p>}
        {content.image && <img src={content.image} alt="Generated content" className="w-full rounded-lg shadow-md" />}
        {content.video && (
          <video src={content.video} controls className="w-full rounded-lg shadow-md mt-4">
            Your browser does not support the video tag.
          </video>
        )}
        {content.meme && <img src={content.meme} alt="Generated meme" className="w-full rounded-lg shadow-md mt-4" />}
      </CardContent>
    </Card>
  );
};

export default OutputSection;

