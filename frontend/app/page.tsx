'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, User, Bot, Loader2, Plus, MessageSquare, PanelLeftClose, PanelLeft, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

export default function Home() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your AI Tutor. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load sessions from localStorage on mount
  useEffect(() => {
    const savedSessions = localStorage.getItem('chatSessions');
    if (savedSessions) {
      const parsed = JSON.parse(savedSessions);
      setSessions(parsed.map((s: ChatSession) => ({ ...s, createdAt: new Date(s.createdAt) })));
    }
  }, []);

  // Save sessions to localStorage whenever they change
  useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem('chatSessions', JSON.stringify(sessions));
    }
  }, [sessions]);

  // Update current session's messages
  useEffect(() => {
    if (currentSessionId && messages.length > 1) {
      setSessions(prev => prev.map(session => 
        session.id === currentSessionId 
          ? { ...session, messages, title: getSessionTitle(messages) }
          : session
      ));
    }
  }, [messages, currentSessionId]);

  const getSessionTitle = (msgs: Message[]): string => {
    const firstUserMessage = msgs.find(m => m.role === 'user');
    if (firstUserMessage) {
      return firstUserMessage.content.slice(0, 30) + (firstUserMessage.content.length > 30 ? '...' : '');
    }
    return 'New Chat';
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const createNewChat = () => {
    const newSession: ChatSession = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [{ role: 'assistant', content: 'Hello! I am your AI Tutor. How can I help you today?' }],
      createdAt: new Date()
    };
    setSessions(prev => [newSession, ...prev]);
    setCurrentSessionId(newSession.id);
    setMessages(newSession.messages);
  };

  const selectSession = (session: ChatSession) => {
    setCurrentSessionId(session.id);
    setMessages(session.messages);
  };

  const deleteSession = (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setSessions(prev => prev.filter(s => s.id !== sessionId));
    if (currentSessionId === sessionId) {
      setCurrentSessionId(null);
      setMessages([{ role: 'assistant', content: 'Hello! I am your AI Tutor. How can I help you today?' }]);
    }
    // Update localStorage
    const remaining = sessions.filter(s => s.id !== sessionId);
    if (remaining.length === 0) {
      localStorage.removeItem('chatSessions');
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      setMessages(prev => [...prev, { role: 'assistant', content: `Uploading & analyzing ${file.name}... (This may take a moment)` }]);

      await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessages(prev => [...prev, { role: 'assistant', content: `✅ ${file.name} processed! I can now answer questions about it.` }]);
    } catch (error) {
      console.error('Upload failed:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: `❌ Failed to upload ${file.name}. Please try again.` }]);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Create a new session if none exists
      if (!currentSessionId) {
        const newSession: ChatSession = {
          id: Date.now().toString(),
          title: userMessage.slice(0, 30) + (userMessage.length > 30 ? '...' : ''),
          messages: [...messages, { role: 'user', content: userMessage }],
          createdAt: new Date()
        };
        setSessions(prev => [newSession, ...prev]);
        setCurrentSessionId(newSession.id);
      }

      // Call through the Next.js rewrite proxy
      const response = await axios.post('/api/chat', {
        message: userMessage,
        session_id: currentSessionId || "web-user-1"
      });

      setMessages(prev => [...prev, { role: 'assistant', content: response.data.answer }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-gray-950 border-r border-gray-800 flex flex-col overflow-hidden`}>
        <div className="p-3 border-b border-gray-800">
          <button
            onClick={createNewChat}
            className="w-full flex items-center gap-2 p-3 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors text-white font-medium"
          >
            <Plus className="w-5 h-5" />
            New Chat
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {sessions.map(session => (
            <div
              key={session.id}
              onClick={() => selectSession(session)}
              className={`group flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-colors ${
                currentSessionId === session.id
                  ? 'bg-gray-800 border border-gray-700'
                  : 'hover:bg-gray-800/50'
              }`}
            >
              <MessageSquare className="w-4 h-4 text-gray-400 flex-shrink-0" />
              <span className="flex-1 text-sm truncate text-gray-300">{session.title}</span>
              <button
                onClick={(e) => deleteSession(session.id, e)}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-700 rounded transition-all"
              >
                <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-400" />
              </button>
            </div>
          ))}
          {sessions.length === 0 && (
            <p className="text-center text-gray-500 text-sm py-4">No chat history</p>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="p-4 border-b border-gray-800 bg-gray-900 sticky top-0 z-10">
          <div className="max-w-4xl mx-auto flex items-center gap-2">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors mr-2"
            >
              {sidebarOpen ? (
                <PanelLeftClose className="w-5 h-5 text-gray-400" />
              ) : (
                <PanelLeft className="w-5 h-5 text-gray-400" />
              )}
            </button>
            <div className="p-2 bg-blue-600 rounded-lg">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent flex-1">
              AI Personal Tutor
            </h1>
          </div>
        </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''
                }`}
            >
              <div
                className={`p-2 rounded-full flex-shrink-0 ${msg.role === 'user' ? 'bg-purple-600' : 'bg-blue-600'
                  }`}
              >
                {msg.role === 'user' ? (
                  <User className="w-5 h-5 text-white" />
                ) : (
                  <Bot className="w-5 h-5 text-white" />
                )}
              </div>


              <div
                className={`p-4 rounded-2xl max-w-[80%] ${msg.role === 'user'
                  ? 'bg-purple-600/20 border border-purple-500/30 rounded-tr-none'
                  : 'bg-gray-800 border border-gray-700 rounded-tl-none'
                  }`}
              >
                {msg.role === 'user' ? (
                  <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                ) : (
                  <div className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-full bg-blue-600 flex-shrink-0">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="p-4 rounded-2xl bg-gray-800 border border-gray-700 rounded-tl-none flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
                <span className="text-gray-400 text-sm">Thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="p-4 border-t border-gray-800 bg-gray-900 sticky bottom-0">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="hidden"
              accept=".pdf"
            />

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              className="w-full p-4 pl-12 pr-12 rounded-xl bg-gray-800 border border-gray-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-500"
              disabled={isLoading}
            />

            {/* Left: Upload Button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading || isLoading}
              className="absolute left-2 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
              title="Upload PDF"
            >
              {isUploading ? (
                <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
              ) : (
                <Plus className="w-5 h-5" />
              )}
            </button>

            {/* Right: Send Button */}
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <p className="text-center text-xs text-gray-500 mt-2">
            AI can make mistakes. Please verify important information.
          </p>
        </div>
      </footer>
      </div>
    </div>
  );
}
