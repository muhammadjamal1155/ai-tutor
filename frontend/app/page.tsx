'use client';

import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Toast, Attachment, UploadedPDF, Message, ChatSession } from './types';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { ChatArea } from './components/ChatArea';
import { ChatInput } from './components/ChatInput';
import { SearchModal } from './components/SearchModal';
import { ToastContainer } from './components/ToastContainer';

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
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [useAI, setUseAI] = useState(true);
  const [responseMode, setResponseMode] = useState<'ai' | 'document_only'>('ai');
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

  useEffect(() => {
    const savedSessions = localStorage.getItem('chatSessions');
    if (savedSessions) {
      const parsed = JSON.parse(savedSessions);
      const loadedSessions = parsed.map((s: ChatSession) => ({ ...s, createdAt: new Date(s.createdAt) }));
      setSessions(loadedSessions);

      const lastSessionId = localStorage.getItem('currentSessionId');
      if (lastSessionId) {
        const lastSession = loadedSessions.find((s: ChatSession) => s.id === lastSessionId);
        if (lastSession) {
          setCurrentSessionId(lastSessionId);
          setMessages(lastSession.messages);
        }
      }
    }

    const savedPDFs = localStorage.getItem('uploadedPDFs');
    if (savedPDFs) {
      const parsed = JSON.parse(savedPDFs);
      setUploadedPDFs(parsed.map((p: UploadedPDF) => ({ ...p, uploadedAt: new Date(p.uploadedAt) })));
    }
  }, []);

  useEffect(() => {
    if (currentSessionId) {
      localStorage.setItem('currentSessionId', currentSessionId);
    }
  }, [currentSessionId]);

  useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem('chatSessions', JSON.stringify(sessions));
    }
  }, [sessions]);

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

  const handleSummarize = (pdf: UploadedPDF, e: React.MouseEvent) => {
    e.stopPropagation();
    const prompt = `Please provide a detailed summary of the document '${pdf.name}'. \n\nInclude:\n1. Key Concepts\n2. Detailed Summary\n3. Key Takeaways`;
    setInput(prompt);
    // Don't auto-submit, let user confirm or edit
    if (fileInputRef.current) fileInputRef.current.focus();
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

      const response = await axios.post('/api/chat', {
        message: userMessage || `Please analyze and summarize the document: ${attachment?.name}`,
        session_id: currentSessionId || "web-user-1",
        use_ai: useAI
      });

      if (response.data.mode) {
        setResponseMode(response.data.mode);
        if (response.data.mode === 'document_only' && useAI) {
          showToast('error', 'AI quota exceeded. Showing document results instead.');
        }
      }

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
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      <SearchModal
        isOpen={searchOpen}
        onClose={() => setSearchOpen(false)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        sessions={sessions}
        onSelectSession={selectSession}
      />

      <Sidebar
        isOpen={sidebarOpen}
        setIsOpen={setSidebarOpen}
        sessions={sessions}
        currentSessionId={currentSessionId}
        createNewChat={createNewChat}
        selectSession={selectSession}
        deleteSession={deleteSession}
        openSearch={() => setSearchOpen(true)}
        uploadedPDFs={uploadedPDFs}
        selectPDFFromLibrary={selectPDFFromLibrary}
        deletePDF={deletePDF}
        onSummarize={handleSummarize}
      />

      <div className="flex-1 flex flex-col">
        <Header
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          useAI={useAI}
          setUseAI={setUseAI}
        />

        <ChatArea
          messages={messages}
          isLoading={isLoading}
          messagesEndRef={messagesEndRef as React.RefObject<HTMLDivElement>}
        />

        <ChatInput
          input={input}
          setInput={setInput}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
          isUploading={isUploading}
          handleFileUpload={handleFileUpload}
          pendingAttachment={pendingAttachment}
          removePendingAttachment={removePendingAttachment}
          fileInputRef={fileInputRef as React.RefObject<HTMLInputElement>}
        />
      </div>
    </div>
  );
}
