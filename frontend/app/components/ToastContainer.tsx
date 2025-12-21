import React from 'react';
import { CheckCircle, XCircle, X } from 'lucide-react';
import { Toast } from '../types';

interface ToastContainerProps {
    toasts: Toast[];
    removeToast: (id: string) => void;
}

export const ToastContainer: React.FC<ToastContainerProps> = ({ toasts, removeToast }) => {
    return (
        <div className="fixed top-4 right-4 z-50 space-y-2">
            {toasts.map(toast => (
                <div
                    key={toast.id}
                    className={`flex items-center gap-3 p-4 rounded-lg shadow-lg animate-in slide-in-from-right duration-300 ${toast.type === 'success'
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
    );
};
