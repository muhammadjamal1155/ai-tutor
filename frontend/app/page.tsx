'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, User, Bot, Loader2, Plus, MessageSquare, PanelLeftClose, PanelLeft, Trash2, CheckCircle, XCircle, X, FileText, Search, Library, SquarePen, ChevronDown, ChevronRight } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Toast {
  id: string;
  type: 'success' | 'error';
  message: string;
}

interface Attachment {
  name: string;
  type: string;
}

interface UploadedPDF {
  id: string;
  name: string;
  uploadedAt: Date;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  attachment?: Attachment;
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
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [pendingAttachment, setPendingAttachment] = useState<Attachment | null>(null);
  const [uploadedPDFs, setUploadedPDFs] = useState<UploadedPDF[]>([]);
  const [libraryOpen, setLibraryOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const showToast = (type: 'success' | 'error', message: string) => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 5000);
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  // Load sessions from localStorage on mount
  useEffect(() => {
    const savedSessions = localStorage.getItem('chatSessions');
    if (savedSessions) {
      const parsed = JSON.parse(savedSessions);
      setSessions(parsed.map((s: ChatSession) => ({ ...s, createdAt: new Date(s.createdAt) })));
    }
    
    const savedPDFs = localStorage.getItem('uploadedPDFs');
    if (savedPDFs) {
      const parsed = JSON.parse(savedPDFs);
      setUploadedPDFs(parsed.map((p: UploadedPDF) => ({ ...p, uploadedAt: new Date(p.uploadedAt) })));
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
      await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Add to uploaded PDFs list
      const newPDF: UploadedPDF = {
        id: Date.now().toString(),
        name: file.name,
        uploadedAt: new Date()
      };
      setUploadedPDFs(prev => {
        const updated = [newPDF, ...prev.filter(p => p.name !== file.name)];
        localStorage.setItem('uploadedPDFs', JSON.stringify(updated));
        return updated;
      });

      // Set pending attachment to show in input bar
      setPendingAttachment({ name: file.name, type: 'pdf' });
      showToast('success', `${file.name} uploaded! Ask a question about it.`);
    } catch (error) {
      console.error('Upload failed:', error);
      showToast('error', `Failed to upload ${file.name}. Please try again.`);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const removePendingAttachment = () => {
    setPendingAttachment(null);
  };

  const deletePDF = (pdfId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setUploadedPDFs(prev => {
      const updated = prev.filter(p => p.id !== pdfId);
      if (updated.length === 0) {
        localStorage.removeItem('uploadedPDFs');
      } else {
        localStorage.setItem('uploadedPDFs', JSON.stringify(updated));
      }
      return updated;
    });
  };

  const selectPDFFromLibrary = (pdf: UploadedPDF) => {
    setPendingAttachment({ name: pdf.name, type: 'pdf' });
    showToast('success', `${pdf.name} selected. Ask a question about it!`);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if ((!input.trim() && !pendingAttachment) || isLoading) return;

    const userMessage = input;
    const attachment = pendingAttachment;
    setInput('');
    setPendingAttachment(null);
    
    const newUserMessage: Message = { 
      role: 'user', 
      content: userMessage || (attachment ? `Analyze this document: ${attachment.name}` : ''),
      attachment: attachment || undefined
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      // Create a new session if none exists
      if (!currentSessionId) {
        const newSession: ChatSession = {
          id: Date.now().toString(),
          title: (userMessage || attachment?.name || 'New Chat').slice(0, 30) + ((userMessage || attachment?.name || '').length > 30 ? '...' : ''),
          messages: [...messages, newUserMessage],
          createdAt: new Date()
        };
        setSessions(prev => [newSession, ...prev]);
        setCurrentSessionId(newSession.id);
      }

      // Call through the Next.js rewrite proxy
      const response = await axios.post('/api/chat', {
        message: userMessage || `Please analyze and summarize the document: ${attachment?.name}`,
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
      {/* Toast Notifications */}
      <div className="fixed top-4 right-4 z-50 space-y-2">
        {toasts.map(toast => (
          <div
            key={toast.id}
            className={`flex items-center gap-3 p-4 rounded-lg shadow-lg animate-in slide-in-from-right duration-300 ${
              toast.type === 'success'
                ? 'bg-green-600/90 border border-green-500'
                : 'bg-red-600/90 border border-red-500'
            }`}
          >
            {toast.type === 'success' ? (
              <CheckCircle className="w-5 h-5 text-white flex-shrink-0" />
            ) : (
              <XCircle className="w-5 h-5 text-white flex-shrink-0" />
            )}
            <span className="text-white text-sm max-w-xs">{toast.message}</span>
            <button
              onClick={() => removeToast(toast.id)}
              className="p-1 hover:bg-white/20 rounded transition-colors"
            >
              <X className="w-4 h-4 text-white" />
            </button>
          </div>
        ))}
      </div>

      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-gray-950 flex flex-col overflow-hidden`}>
        {/* Logo and Toggle */}
        <div className="p-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
              <Bot className="w-5 h-5 text-gray-900" />
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
          >
            <PanelLeftClose className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Navigation Items */}
        <div className="px-2 space-y-1">
          <button
            onClick={createNewChat}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-800 transition-colors text-gray-200"
          >
            <SquarePen className="w-5 h-5" />
            <span className="text-sm">New chat</span>
          </button>
          
          <button
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-800 transition-colors text-gray-200"
          >
            <Search className="w-5 h-5" />
            <span className="text-sm">Search chats</span>
          </button>
          
          {/* Library Section */}
          <div>
            <button
              onClick={() => setLibraryOpen(!libraryOpen)}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-800 transition-colors text-gray-200"
            >
              <Library className="w-5 h-5" />
              <span className="text-sm flex-1 text-left">Library</span>
              {uploadedPDFs.length > 0 && (
                <span className="text-xs bg-gray-700 px-1.5 py-0.5 rounded text-gray-400">
                  {uploadedPDFs.length}
                </span>
              )}
              {libraryOpen ? (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronRight className="w-4 h-4 text-gray-400" />
              )}
            </button>
            
            {/* PDF List */}
            {libraryOpen && (
              <div className="mt-1 ml-4 space-y-1">
                {uploadedPDFs.length === 0 ? (
                  <p className="px-3 py-2 text-xs text-gray-500">No documents uploaded</p>
                ) : (
                  uploadedPDFs.map(pdf => (
                    <div
                      key={pdf.id}
                      onClick={() => selectPDFFromLibrary(pdf)}
                      className="group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-800/50 transition-colors"
                    >
                      <FileText className="w-4 h-4 text-rose-400 flex-shrink-0" />
                      <span className="flex-1 text-xs truncate text-gray-400">{pdf.name}</span>
                      <button
                        onClick={(e) => deletePDF(pdf.id, e)}
                        className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-700 rounded transition-all"
                      >
                        <Trash2 className="w-3 h-3 text-gray-400 hover:text-red-400" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>

        {/* Divider */}
        <div className="my-3 border-t border-gray-800" />
        
        {/* Chat History */}
        <div className="flex-1 overflow-y-auto px-2 space-y-1">
          {sessions.length > 0 && (
            <p className="px-3 py-2 text-xs text-gray-500 font-medium">Recent</p>
          )}
          {sessions.map(session => (
            <div
              key={session.id}
              onClick={() => selectSession(session)}
              className={`group flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer transition-colors ${
                currentSessionId === session.id
                  ? 'bg-gray-800'
                  : 'hover:bg-gray-800/50'
              }`}
            >
              <span className="flex-1 text-sm truncate text-gray-300">{session.title}</span>
              <button
                onClick={(e) => deleteSession(session.id, e)}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-700 rounded transition-all"
              >
                <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-400" />
              </button>
            </div>
          ))}
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
                {/* Show attachment if exists */}
                {msg.attachment && (
                  <div className="flex items-center gap-2 mb-3 p-2 bg-gray-700/50 border border-gray-600 rounded-lg w-fit">
                    <div className="p-1.5 bg-rose-500 rounded">
                      <FileText className="w-4 h-4 text-white" />
                    </div>
                    <div className="text-sm">
                      <p className="text-gray-100 font-medium">{msg.attachment.name}</p>
                      <p className="text-gray-400 text-xs uppercase">{msg.attachment.type}</p>
                    </div>
                  </div>
                )}
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
          {/* Pending Attachment Preview */}
          {pendingAttachment && (
            <div className="mb-2 flex items-center gap-2">
              <div className="flex items-center gap-2 px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg">
                <div className="p-1.5 bg-rose-500 rounded">
                  <FileText className="w-4 h-4 text-white" />
                </div>
                <div className="text-sm">
                  <p className="text-gray-100 font-medium">{pendingAttachment.name}</p>
                  <p className="text-gray-400 text-xs uppercase">{pendingAttachment.type}</p>
                </div>
                <button
                  type="button"
                  onClick={removePendingAttachment}
                  className="ml-1 p-1 hover:bg-gray-600 rounded transition-colors"
                >
                  <X className="w-4 h-4 text-gray-400 hover:text-white" />
                </button>
              </div>
            </div>
          )}
          
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
              placeholder={pendingAttachment ? "Ask a question about this document..." : "Ask a question..."}
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
              disabled={(!input.trim() && !pendingAttachment) || isLoading}
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
