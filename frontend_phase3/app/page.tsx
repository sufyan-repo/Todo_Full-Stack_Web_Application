'use client';
import { useState, useRef, useEffect } from 'react';
import Head from 'next/head';
import Image from 'next/image';

export default function ChatPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState('');
  const messagesEndRef = useRef(null);

  // Initialize with a sample user ID (in a real app, this would come from auth)
  useEffect(() => {
    const sampleUserId = 'user-' + Math.random().toString(36).substr(2, 9);
    setUserId(sampleUserId);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = { id: Date.now(), role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await fetch(`http://localhost:8023/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input, user_id: userId }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from chat API');
      }

      const data = await response.json();

      // Add assistant message to chat
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        toolCalls: data.tool_calls
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Phase 3 AI Chatbot</title>
        <meta name="description" content="AI-powered todo assistant" />
      </Head>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="mb-8 flex flex-col items-center">
          <div className="mb-4">
            <Image
              src="/todo-ai-logo.svg"
              alt="AI Todo Assistant Logo"
              width={80}
              height={80}
              className="mx-auto"
            />
          </div>
          <h1 className="text-3xl font-bold text-gray-800">AI Todo Assistant</h1>
          <p className="text-gray-600 mt-2">Manage your todos with natural language</p>
          {userId && <p className="text-sm text-gray-500 mt-1">User ID: {userId}</p>}
        </header>

        <div className="bg-white rounded-lg shadow-md mb-6">
          <div className="border-b border-gray-200 p-4 flex items-center">
            <div className="w-3 h-3 rounded-full bg-red-400 mr-2"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-400 mr-2"></div>
            <div className="w-3 h-3 rounded-full bg-green-400 mr-2"></div>
            <h2 className="text-lg font-semibold text-gray-800 ml-2">Chat</h2>
          </div>

          <div className="p-4 h-[500px] overflow-y-auto">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-gray-500">
                <p className="mb-4">Welcome to the AI Todo Assistant!</p>
                <p className="text-sm">Try asking me to:</p>
                <ul className="mt-2 text-left list-disc pl-5 space-y-1">
                  <li>Add a new task</li>
                  <li>List your tasks</li>
                  <li>Mark a task as complete</li>
                  <li>Delete a task</li>
                </ul>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`p-4 rounded-lg ${msg.role === 'user' ? 'bg-blue-50 ml-10' : 'bg-gray-100 mr-10'}`}
                  >
                    <div className="font-medium text-sm mb-1 flex items-center">
                      {msg.role === 'user' ? (
                        <>
                          <span className="w-2 h-2 rounded-full bg-blue-500 mr-2"></span>
                          You
                        </>
                      ) : (
                        <>
                          <span className="w-2 h-2 rounded-full bg-purple-500 mr-2"></span>
                          AI Assistant
                        </>
                      )}
                    </div>
                    <div className="text-gray-800">{msg.content}</div>

                    {msg.toolCalls && msg.toolCalls.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <div className="text-xs text-gray-500 mb-1">Tool Calls:</div>
                        {msg.toolCalls.map((call, idx) => (
                          <div key={idx} className="text-xs bg-gray-200 p-2 rounded mt-1">
                            <div className="font-mono">{call.name}(...)</div>
                            {call.result && (
                              <div className="mt-1 text-gray-600">
                                Result: {typeof call.result === 'object'
                                  ? JSON.stringify(call.result)
                                  : call.result}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className="p-4 rounded-lg bg-gray-100 mr-10">
                    <div className="font-medium text-sm mb-1 flex items-center">
                      <span className="w-2 h-2 rounded-full bg-purple-500 mr-2"></span>
                      AI Assistant
                    </div>
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                      <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-75"></div>
                      <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-150"></div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me to manage your tasks..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Send
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            Examples: "Add a task to buy groceries", "Show my tasks", "Complete task #1"
          </div>
        </form>
      </main>
    </div>
  );
}