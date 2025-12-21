import React, { useRef, useEffect } from 'react';
import { X } from 'lucide-react';
import { ChatSession } from '../types';

interface SearchModalProps {
    isOpen: boolean;
    onClose: () => void;
    searchQuery: string;
    setSearchQuery: (query: string) => void;
    sessions: ChatSession[];
    onSelectSession: (session: ChatSession) => void;
}

export const SearchModal: React.FC<SearchModalProps> = ({
    isOpen, onClose, searchQuery, setSearchQuery, sessions, onSelectSession
}) => {
    const searchInputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (isOpen) {
            setTimeout(() => searchInputRef.current?.focus(), 100);
        }
    }, [isOpen]);

    if (!isOpen) return null;

    const filteredSessions = searchQuery.trim()
        ? sessions.filter(s =>
            s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            s.messages.some(m => m.content.toLowerCase().includes(searchQuery.toLowerCase()))
        )
        : sessions;

    const getMatchPreview = (session: ChatSession): string => {
        if (!searchQuery.trim()) return session.title;
        const query = searchQuery.toLowerCase();
        for (const msg of session.messages) {
            const idx = msg.content.toLowerCase().indexOf(query);
            if (idx !== -1) {
                const start = Math.max(0, idx - 30);
                const end = Math.min(msg.content.length, idx + query.length + 50);
                return (start > 0 ? '...' : '') + msg.content.slice(start, end) + (end < msg.content.length ? '...' : '');
            }
        }
        return session.title;
    };

    const highlightMatch = (text: string): React.ReactElement => {
        if (!searchQuery.trim()) return <>{text}</>;
        const query = searchQuery.toLowerCase();
        const idx = text.toLowerCase().indexOf(query);
        if (idx === -1) return <>{text}</>;
        return (
            <>
                {text.slice(0, idx)}
                <span className="font-semibold text-white">{text.slice(idx, idx + searchQuery.length)}</span>
                {text.slice(idx + searchQuery.length)}
            </>
        );
    };

    return (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/60 backdrop-blur-sm">
            <div className="w-full max-w-xl bg-gray-900 rounded-xl shadow-2xl border border-gray-700 overflow-hidden">
                {/* Search Input */}
                <div className="flex items-center gap-3 p-4 border-b border-gray-800">
                    <div className="flex-1 relative">
                        {searchQuery && (
                            <span className="inline-block bg-blue-600 text-white text-sm px-2 py-0.5 rounded mr-2">
                                {searchQuery}
                            </span>
                        )}
                        <input
                            ref={searchInputRef}
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Search conversations..."
                            className="w-full bg-transparent text-gray-200 text-base focus:outline-none placeholder:text-gray-500"
                        />
                    </div>
                    <button
                        onClick={() => {
                            onClose();
                            setSearchQuery('');
                        }}
                        className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
                    >
                        <X className="w-5 h-5 text-gray-400" />
                    </button>
                </div>

                {/* Search Results */}
                <div className="max-h-96 overflow-y-auto">
                    {filteredSessions.length > 0 ? (
                        filteredSessions.map(session => (
                            <div
                                key={session.id}
                                onClick={() => {
                                    onSelectSession(session);
                                    onClose();
                                    setSearchQuery('');
                                }}
                                className="flex items-start gap-3 px-4 py-3 hover:bg-gray-800 cursor-pointer transition-colors border-b border-gray-800/50 last:border-b-0"
                            >
                                <div className="mt-1 w-4 h-4 rounded-full border-2 border-gray-600 flex-shrink-0" />
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-gray-200 truncate">
                                        {highlightMatch(session.title)}
                                    </p>
                                    <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                                        {highlightMatch(getMatchPreview(session))}
                                    </p>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="px-4 py-8 text-center text-gray-500">
                            {searchQuery.trim() ? 'No chats found' : 'No conversations yet'}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
