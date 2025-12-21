import React from 'react';
import { User, Bot, Loader2, FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message } from '../types';

interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
    messagesEndRef: React.RefObject<HTMLDivElement>;
}

export const ChatArea: React.FC<ChatAreaProps> = ({ messages, isLoading, messagesEndRef }) => {
    return (
        <main className="flex-1 overflow-y-auto p-4 space-y-4">
            <div className="max-w-4xl mx-auto space-y-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex items-start gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                        <div
                            className={`p-2 rounded-full flex-shrink-0 ${msg.role === 'user' ? 'bg-purple-600' : 'bg-blue-600'}`}
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
    );
};
