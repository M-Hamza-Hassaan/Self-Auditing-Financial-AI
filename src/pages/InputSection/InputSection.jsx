import React, { useState } from 'react';
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

const InputSection = ({ onGenerate }) => {
  const [input, setInput] = useState('');
  const [contentType, setContentType] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input && contentType) {
      onGenerate({ input, contentType });
    }
  };

  return (
    <Card className="input-section">
      <CardHeader>
        <CardTitle>Generate Content</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="Enter your content idea"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            required
          />
          <Select onValueChange={setContentType} required>
            <SelectTrigger>
              <SelectValue placeholder="Select content type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="text">Text</SelectItem>
              <SelectItem value="image">Image</SelectItem>
              <SelectItem value="video">Video</SelectItem>
              <SelectItem value="meme">Meme</SelectItem>
            </SelectContent>
          </Select>
          <Button type="submit" className="w-full">Generate</Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default InputSection;

