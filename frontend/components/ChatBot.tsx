'use client';

import { useState, useRef, useEffect } from 'react';
import { X, Bot, Send, User } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: any[];
  timestamp: Date;
}

interface ChatBotProps {
  userId: string;
}

export default function ChatBot({ userId }: ChatBotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Send message to backend - using environment variable or default to port 8000
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/api/${userId}/chat`, {
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
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        toolCalls: data.tool_calls,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-8 right-8 z-50 w-14 h-14 rounded-full bg-primary text-white shadow-lg shadow-primary/30 flex items-center justify-center hover:scale-110 transition-transform duration-300"
          aria-label="Open chat"
        >
          <Bot className="w-6 h-6" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-8 right-8 z-50 w-full max-w-md h-[500px] flex flex-col border border-ui-border/20 rounded-2xl overflow-hidden shadow-2xl bg-background">
          {/* Header */}
          <div className="bg-primary text-white p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bot className="w-5 h-5" />
              <span className="font-bold">AI Todo Assistant</span>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
              aria-label="Close chat"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 bg-muted/5">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center text-muted-foreground">
                <Bot className="w-12 h-12 mb-4 opacity-50" />
                <h3 className="text-lg font-bold mb-2">AI Todo Assistant</h3>
                <p className="text-sm max-w-xs">
                  Manage your tasks with natural language. Try asking me to add, list, complete, or delete tasks.
                </p>
                <div className="mt-4 text-xs bg-primary/10 p-3 rounded-lg w-full">
                  <p className="font-medium mb-1">Examples:</p>
                  <ul className="text-left space-y-1">
                    <li>• "Add a task to buy groceries"</li>
                    <li>• "Show my tasks"</li>
                    <li>• "Complete task #1"</li>
                    <li>• "Delete task #2"</li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user'
                          ? 'bg-primary text-primary-foreground rounded-br-md'
                          : 'bg-card text-card-foreground rounded-bl-md'
                        }`}
                    >
                      <div className="flex items-start gap-2">
                        {msg.role === 'assistant' && <Bot className="w-4 h-4 mt-0.5 flex-shrink-0" />}
                        <div className="flex-1">
                          <div className="font-medium text-sm mb-1">
                            {msg.role === 'user' ? 'You' : 'AI Assistant'}
                          </div>
                          <div className="text-sm">{msg.content}</div>

                          {msg.toolCalls && msg.toolCalls.length > 0 && (
                            <div className="mt-2 pt-2 border-t border-current/20">
                              <div className="text-xs opacity-70 mb-1">Tool Calls:</div>
                              {msg.toolCalls.map((call, idx) => (
                                <div key={idx} className="text-xs bg-current/10 p-2 rounded mt-1 font-mono">
                                  <div>{call.name}(...)</div>
                                  {call.result && (
                                    <div className="mt-1 truncate">
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
                        {msg.role === 'user' && <User className="w-4 h-4 mt-0.5 flex-shrink-0" />}
                      </div>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="max-w-[80%] rounded-2xl rounded-bl-md bg-card text-card-foreground p-4">
                      <div className="flex items-center gap-2">
                        <Bot className="w-4 h-4 mt-0.5" />
                        <div className="font-medium text-sm">AI Assistant</div>
                      </div>
                      <div className="flex space-x-1 pt-2">
                        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"></div>
                        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce delay-75"></div>
                        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce delay-150"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit} className="border-t border-ui-border/20 p-4 bg-card">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me to manage your tasks..."
                className="flex-1 px-4 py-3 border border-input rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 bg-background"
                disabled={isLoading}
                autoFocus
              />
              <Button
                type="submit"
                variant="primary"
                size="sm"
                disabled={isLoading || !input.trim()}
                className="h-12 px-4"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
            <div className="mt-2 text-xs text-muted-foreground">
              Examples: "Add task to buy groceries", "Show my tasks", "Complete task #1"
            </div>
          </form>
        </div>
      )}
    </>
  );
}