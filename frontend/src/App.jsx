import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import './index.css';

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hello! I am your persona-adaptive support agent. How can I help you today?', persona: 'general_user' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (text) => {
    const userMessage = { role: 'user', text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          history: messages.map(m => ({ query: m.text, persona: m.persona }))
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }

      const data = await response.json();
      
      const assistantMessage = {
        role: 'assistant',
        text: data.response,
        persona: data.persona,
        escalated: data.escalated
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [...prev, {
        role: 'assistant',
        text: 'Sorry, I encountered an error. Please make sure the backend is running.',
        persona: 'general_user'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Adaptive Support Agent</h1>
      </header>
      <ChatWindow
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
