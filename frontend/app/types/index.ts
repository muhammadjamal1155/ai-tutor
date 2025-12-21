export interface Toast {
    id: string;
    type: 'success' | 'error';
    message: string;
}

export interface Attachment {
    name: string;
    type: string;
}

export interface UploadedPDF {
    id: string;
    name: string;
    uploadedAt: Date;
}

export interface Message {
    role: 'user' | 'assistant';
    content: string;
    attachment?: Attachment;
}

export interface ChatSession {
    id: string;
    title: string;
    messages: Message[];
    createdAt: Date;
}
