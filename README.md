<div align="center">

# 🎓 AI Personal Tutor

**A personalized AI Learning Tutor powered by RAG, Memory, and Agentic Planning**

*Built with Google Gemini • LangChain • FAISS • Next.js*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-Powered-orange?style=for-the-badge)](https://langchain.com)

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🔧 Backend

| Feature | Description |
|---------|-------------|
| 📄 **PDF Ingestion** | Automatically process PDF study materials |
| ⚡ **Incremental Indexing** | Fast uploads without full re-indexing |
| 🧠 **Intelligent RAG** | Google Gemini + FAISS vector search |
| 💬 **Context-Aware** | Answers from *your* documents only |
| 🔄 **Memory** | Retains conversation context |
| 🌐 **REST API** | FastAPI with `/chat` & `/upload` |

</td>
<td width="50%" valign="top">

### 🎨 Frontend

| Feature | Description |
|---------|-------------|
| 🌙 **Modern UI** | ChatGPT-style dark theme |
| 📚 **Sidebar** | New chat, search, library |
| 🔍 **Search** | Find conversations instantly |
| 📁 **PDF Library** | Manage uploaded documents |
| 💾 **Persistence** | Sessions survive page reload |
| 🔔 **Notifications** | Toast feedback for actions |

</td>
</tr>
</table>

---

## 📁 Project Structure

```
ai-tutor/
│
├── 📂 data/                     # Knowledge Base
│   ├── 📥 raw_pdfs/             # Drop your PDFs here
│   ├── 📄 processed_text/       # Extracted text
│   └── 🧠 embeddings/           # FAISS vector index
│
├── 📂 src/                      # Backend (Python)
│   ├── api/                     # FastAPI server
│   ├── agent/                   # LangChain Tutor Agent
│   ├── config/                  # Settings
│   ├── loaders/                 # PDF processing
│   ├── memory/                  # Conversation memory
│   ├── rag/                     # Vector store logic
│   └── utils/                   # Utilities
│
├── 📂 frontend/                 # Frontend (Next.js)
│   ├── app/                     # App router pages
│   └── public/                  # Static assets
│
└── 📂 tests/                    # Unit tests
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))

### 1️⃣ Clone & Install

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-tutor.git
cd ai-tutor

# Backend setup
python -m venv env
.\env\Scripts\Activate.ps1      # Windows
# source env/bin/activate       # Linux/Mac
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

### 2️⃣ Configure

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 3️⃣ Build Knowledge Base

```bash
# Add PDFs to data/raw_pdfs/, then run:
python src/ingest.py
```

### 4️⃣ Launch

Open **two terminals**:

```bash
# Terminal 1 - Backend (from root)
uvicorn src.api.server:app --reload
```

```bash
# Terminal 2 - Frontend (from frontend/)
npm run dev
```

### 5️⃣ Open App

🌐 Navigate to **[http://localhost:3000](http://localhost:3000)**

---

## 🔌 API Reference

| Endpoint | Method | Description | Body |
|----------|--------|-------------|------|
| `/health` | `GET` | Health check | - |
| `/chat` | `POST` | Send message | `{ "message": "...", "session_id": "..." }` |
| `/upload` | `POST` | Upload PDF | `multipart/form-data` |

---

## 🎯 UI Overview

| Action | How |
|--------|-----|
| ➕ **New Chat** | Click "New chat" in sidebar |
| 🔍 **Search** | Click "Search chats" → type query |
| 📚 **Library** | Expand "Library" to view PDFs |
| 📎 **Upload** | Click 📎 or drag PDF to input |
| 🗑️ **Delete** | Hover chat/PDF → click trash icon |

---

## 📍 Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ | PDF Loading & Vector Database |
| 2 | ✅ | Basic RAG Chatbot |
| 3 | ✅ | Conversation Memory |
| 4 | ✅ | FastAPI REST API |
| 5 | ✅ | Next.js Modern UI |
| 6 | ✅ | Session Persistence & Search |
| 7 | ⬜ | Multi-user Authentication |
| 8 | ⬜ | Advanced Agentic Planning |

---

## 🧪 Testing

```bash
python -m pytest tests -v
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ using Google Gemini & LangChain**

</div>
