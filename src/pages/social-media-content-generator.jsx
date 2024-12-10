'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Navbar from './Navbar'
import Chatbot from './Chatbot'
import './input-section.css'
import './output-section.css'
import './refinement-section.css'

export default function SocialMediaContentGenerator() {
  const [input, setInput] = useState('')
  const [responseType, setResponseType] = useState('')
  const [socialMedia, setSocialMedia] = useState('')
  const [output, setOutput] = useState('')
  const [refinedOutput, setRefinedOutput] = useState('')
  const [showRefinement, setShowRefinement] = useState(false)

  const handleEnter = () => {
    // Simulate generating a response
    setOutput(`Generated ${responseType} content for ${socialMedia}: "${input}"`)
    setShowRefinement(false)
    setRefinedOutput('')
  }

  const handleRefinement = () => {
    // Simulate refining the output
    setRefinedOutput(`Refined ${responseType} content for ${socialMedia}: "${input}" (Enhanced version)`)
    setShowRefinement(true)
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <div className="flex-grow flex">
        <div className="w-1/2 p-4">
          <Card className="input-section">
            <CardHeader>
              <CardTitle>Input Section</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input
                placeholder="Enter your content here"
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <Select onValueChange={setResponseType}>
                <SelectTrigger>
                  <SelectValue placeholder="Select response type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Casual">Casual</SelectItem>
                  <SelectItem value="Professional">Professional</SelectItem>
                  <SelectItem value="Humorous">Humorous</SelectItem>
                  <SelectItem value="Informative">Informative</SelectItem>
                </SelectContent>
              </Select>
              <Select onValueChange={setSocialMedia}>
                <SelectTrigger>
                  <SelectValue placeholder="Select social media platform" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Twitter">Twitter</SelectItem>
                  <SelectItem value="Facebook">Facebook</SelectItem>
                  <SelectItem value="LinkedIn">LinkedIn</SelectItem>
                  <SelectItem value="Instagram">Instagram</SelectItem>
                </SelectContent>
              </Select>
              <Button onClick={handleEnter}>Enter</Button>
            </CardContent>
          </Card>

          {output && (
            <Card className="output-section mt-4">
              <CardHeader>
                <CardTitle>Output Section</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p>{output}</p>
                <Button onClick={handleRefinement}>Refinement</Button>
              </CardContent>
            </Card>
          )}

          {showRefinement && (
            <Card className="refinements-section mt-4">
              <CardHeader>
                <CardTitle>Refinement Section</CardTitle>
              </CardHeader>
              <CardContent>
                <p>{refinedOutput}</p>
              </CardContent>
            </Card>
          )}
        </div>
        <div className="w-1/2">
          <Chatbot />
        </div>
      </div>
    </div>
  )
}

