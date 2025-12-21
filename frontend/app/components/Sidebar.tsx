import React, { useState } from 'react';
import { Bot, PanelLeftClose, SquarePen, Search, Library, ChevronDown, ChevronRight, FileText, Trash2 } from 'lucide-react';
import { ChatSession, UploadedPDF } from '../types';

interface SidebarProps {
    isOpen: boolean;
    setIsOpen: (open: boolean) => void;
    sessions: ChatSession[];
    currentSessionId: string | null;
    createNewChat: () => void;
    selectSession: (session: ChatSession) => void;
    deleteSession: (id: string, e: React.MouseEvent) => void;
    openSearch: () => void;
    uploadedPDFs: UploadedPDF[];
    selectPDFFromLibrary: (pdf: UploadedPDF) => void;
    deletePDF: (id: string, e: React.MouseEvent) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
    isOpen, setIsOpen, sessions, currentSessionId, createNewChat, selectSession, deleteSession, openSearch, uploadedPDFs, selectPDFFromLibrary, deletePDF
}) => {
    const [libraryOpen, setLibraryOpen] = useState(false);

    return (
        <aside className={`${isOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-gray-950 flex flex-col overflow-hidden`}>
            {/* Logo and Toggle */}
            <div className="p-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
                        <Bot className="w-5 h-5 text-white" />
                    </div>
                </div>
                <button
                    onClick={() => setIsOpen(false)}
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

                {/* Search Button */}
                <button
                    onClick={openSearch}
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
                        className={`group flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer transition-colors ${currentSessionId === session.id
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
    );
};
