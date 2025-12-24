import React, { useRef } from 'react';
import { ArrowUp, Plus, Loader2, FileText, X } from 'lucide-react';
import { Attachment } from '../types';

interface ChatInputProps {
    input: string;
    setInput: (value: string) => void;
    handleSubmit: (e: React.FormEvent) => void;
    isLoading: boolean;
    isUploading: boolean;
    handleFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
    pendingAttachment: Attachment | null;
    removePendingAttachment: () => void;
    fileInputRef: React.RefObject<HTMLInputElement>;
}

export const ChatInput: React.FC<ChatInputProps> = ({
    input, setInput, handleSubmit, isLoading, isUploading, handleFileUpload, pendingAttachment, removePendingAttachment, fileInputRef
}) => {
    return (
        <footer className="p-4 border-t border-gray-800 bg-gray-900 sticky bottom-0">
            <div className="max-w-4xl mx-auto">
                <form onSubmit={handleSubmit}>
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                        className="hidden"
                        accept=".pdf"
                    />

                    <div className="bg-gray-800 border border-gray-700 rounded-2xl overflow-hidden focus-within:border-gray-600 transition-all">
                        {/* Pending Attachment Preview - Inside Input */}
                        {pendingAttachment && (
                            <div className="px-4 pt-4">
                                <div className="inline-flex items-center gap-3 px-3 py-2 bg-gray-900 border border-gray-700 rounded-xl">
                                    <div className="p-2 bg-rose-500 rounded-lg">
                                        <FileText className="w-5 h-5 text-white" />
                                    </div>
                                    <div className="text-sm">
                                        <p className="text-gray-100 font-medium">{pendingAttachment.name}</p>
                                        <p className="text-gray-500 text-xs uppercase">{pendingAttachment.type}</p>
                                    </div>
                                    <button
                                        type="button"
                                        onClick={removePendingAttachment}
                                        className="p-1 hover:bg-gray-700 rounded-full transition-colors"
                                    >
                                        <X className="w-4 h-4 text-gray-400 hover:text-white" />
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* Input Row */}
                        <div className="flex items-center gap-2 p-2">
                            {/* Left: Upload Button */}
                            <button
                                type="button"
                                onClick={() => fileInputRef.current?.click()}
                                disabled={isUploading || isLoading}
                                className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors flex-shrink-0"
                                title="Upload PDF"
                            >
                                {isUploading ? (
                                    <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
                                ) : (
                                    <Plus className="w-5 h-5" />
                                )}
                            </button>

                            {/* Text Input */}
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Ask anything"
                                className="flex-1 py-2 px-2 bg-transparent outline-none placeholder:text-gray-500 text-white"
                                disabled={isLoading}
                            />



                            {/* Right: Send Button */}
                            <button
                                type="submit"
                                disabled={(!input.trim() && !pendingAttachment) || isLoading}
                                className="p-2 bg-white text-gray-900 rounded-full hover:bg-gray-200 disabled:opacity-30 disabled:hover:bg-white transition-colors flex-shrink-0"
                            >
                                <ArrowUp className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </form>
                <p className="text-center text-xs text-gray-500 mt-3">
                    AI can make mistakes. Please verify important information.
                </p>
            </div>
        </footer>
    );
};
