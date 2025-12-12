# Personalized AI Tutor

Personalized AI Learning Tutor Using RAG, Memory, and Agentic Planning.

## 🚀 Features (Implemented)
- **PDF Ingestion**: Automatically scans and processes PDF study materials from `data/raw_pdfs`.
- **Intelligent RAG**: Uses **Google Gemini** embeddings and **FAISS** vector database to find relevant notes.
- **Context-Aware Answers**: The AI answers questions using *only* your provided documents, ensuring accurate and relevant explanations.
- **Unit Tested**: Core components (Loader, Database) are verified with automated tests.

## 📦 Project Structure
```text
ai-tutor/
├── data/                  # Your Knowledge Base
│   ├── raw_pdfs/          # 📥 Put your PDF files here
│   └── embeddings/        # 🧠 Vector Database (FAISS index)
├── src/                   # Source Code
│   ├── loaders/           # PDF Processing logic
│   ├── rag/               # Vector Store & Embedding logic
│   └── agent/             # Tutor Intelligence (Chatbot)
└── tests/                 # Unit Tests
```

## 🛠️ Setup & Usage

### 1. Installation
Ensure you have Python 3.10+ installed.
```bash
# Create virtual environment
python -m venv env
.\env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory and add your Google API Key:
```env
GOOGLE_API_KEY=your_api_key_here
```

### 3. Build the Brain (Ingestion)
Whenever you add new PDFs to `data/raw_pdfs`, run:
```bash
python src/ingest.py
```

### 4. Start Tutoring
To chat with your AI Tutor:
```bash
python -m src.agent.tutor
```

### 5. Run Tests
To verify everything is working:
```bash
python -m pytest tests
```

## 📝 Roadmap
- [x] **Phase 1**: PDF Loading & Vector Database
- [x] **Phase 2**: Basic RAG Chatbot
- [ ] **Phase 3**: Conversation Memory (Context Retention)
- [ ] **Phase 4**: Agentic Planning (Complex Reasoning)
- [ ] **Phase 5**: Streamlit User Interface
