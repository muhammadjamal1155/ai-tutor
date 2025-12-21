import React from 'react';
import { Bot, PanelLeft, Sparkles, BookOpen } from 'lucide-react';

interface HeaderProps {
    sidebarOpen: boolean;
    setSidebarOpen: (open: boolean) => void;
    useAI: boolean;
    setUseAI: (use: boolean) => void;
}

export const Header: React.FC<HeaderProps> = ({ sidebarOpen, setSidebarOpen, useAI, setUseAI }) => {
    return (
        <header className="p-4 border-b border-gray-800 bg-gray-900 sticky top-0 z-10">
            <div className="max-w-4xl mx-auto flex items-center gap-2">
                {!sidebarOpen && (
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="p-2 hover:bg-gray-800 rounded-lg transition-colors mr-2"
                    >
                        <PanelLeft className="w-5 h-5 text-gray-400" />
                    </button>
                )}
                <div className="p-2 bg-blue-600 rounded-lg">
                    <Bot className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent flex-1">
                    AI Personal Tutor
                </h1>

                {/* AI Mode Toggle */}
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setUseAI(!useAI)}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium transition-all ${useAI
                                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/25'
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                            }`}
                        title={useAI ? 'AI Mode: Using AI for answers' : 'Document Mode: Searching documents only'}
                    >
                        {useAI ? (
                            <>
                                <Sparkles className="w-4 h-4" />
                                <span>AI Mode</span>
                            </>
                        ) : (
                            <>
                                <BookOpen className="w-4 h-4" />
                                <span>Docs Only</span>
                            </>
                        )}
                    </button>
                </div>
            </div>
        </header>
    );
};
