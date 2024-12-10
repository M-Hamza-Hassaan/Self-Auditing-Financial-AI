'use client'
import { useState } from 'react'
import Navbar from './Navbar/Navbar'
import Chatbot from './Chatbot/Chatbot'
import { Button } from "@/components/ui/button"
import { MessageCircle } from 'lucide-react'

export default function Page() {
  const [isChatbotOpen, setIsChatbotOpen] = useState(true)

  return (
    <main className="flex flex-col min-h-screen">
      <Navbar />
      <div className="flex-grow p-4 relative">
        {isChatbotOpen ? (
          <div className="fixed bottom-4 right-4 w-96 h-[600px]">
            <Chatbot onClose={() => setIsChatbotOpen(false)} />
          </div>
        ) : (
          <Button
            className="fixed bottom-4 right-4"
            onClick={() => setIsChatbotOpen(true)}
          >
            <MessageCircle className="mr-2 h-4 w-4" /> Open Chatbot
          </Button>
        )}
      </div>
    </main>
  )
}

