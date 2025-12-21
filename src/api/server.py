from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.agent.tutor import TutorAgent
from src.ingest import ingest_data, ingest_single_file
import uvicorn
import os
import shutil
import traceback

# Initialize FastAPI app
app = FastAPI(title="AI Tutor API", version="1.0.0")

# Global State
tutor_agent = None
init_error = None

# Request Models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"
    use_ai: bool = True  # Toggle for AI mode vs Document-only mode

class ChatResponse(BaseModel):
    answer: str
    mode: str = "ai"  # "ai" or "document_only"

@app.on_event("startup")
async def startup_event():
    global tutor_agent, init_error
    from src.config.settings import config
    print(f"Server Startup. Using Key: {config.OPENAI_API_KEY[:10]}...", flush=True)
    print("Attempting to initialize Tutor Agent...", flush=True)
    try:
        tutor_agent = TutorAgent()
        print("AI Tutor Agent initialized successfully.", flush=True)
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"CRITICAL ERROR: Failed to initialize Tutor Agent: {error_msg}", flush=True)
        traceback.print_exc()
        init_error = error_msg

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running."""
    status = "ready" if tutor_agent else "failed"
    return {
        "status": status, 
        "error": init_error
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint to interact with the AI Tutor.
    Supports AI mode and document-only mode (fallback).
    """
    global tutor_agent
    
    if not tutor_agent:
        detail_msg = f"Tutor Agent is not initialized. Error: {init_error}"
        raise HTTPException(status_code=503, detail=detail_msg)
    
    # If user explicitly wants document-only mode
    if not request.use_ai:
        try:
            response = tutor_agent.search_documents(request.message)
            return ChatResponse(answer=response, mode="document_only")
        except Exception as e:
            print(f"Error in document search: {e}")
            raise HTTPException(status_code=500, detail=f"Document search failed: {str(e)}")
    
    # Try AI mode first
    try:
        response = tutor_agent.ask(request.message, session_id=request.session_id)
        return ChatResponse(answer=response, mode="ai")
    except Exception as e:
        error_str = str(e)
        print(f"Error processing chat request: {e}")
        traceback.print_exc()
        
        # Check if it's a quota error - fallback to document search
        if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str or "quota" in error_str.lower():
            print("AI quota exceeded, falling back to document search...")
            try:
                fallback_response = tutor_agent.search_documents(request.message)
                return ChatResponse(answer=fallback_response, mode="document_only")
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
                raise HTTPException(status_code=500, detail=f"Both AI and fallback failed: {str(e)}")
        
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF file and add it to the knowledge base (fast incremental update).
    """
    global tutor_agent
    
    # 1. Validate File
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    # 2. Save File
    from src.config.settings import config
    save_path = os.path.join(config.RAW_PDFS_DIR, file.filename)
    
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"File saved to: {save_path}")
        
        # 3. Fast incremental ingestion (only new file)
        print("Starting fast incremental ingestion...")
        success = ingest_single_file(save_path)
        
        if not success:
            raise Exception("Failed to process document")
        
        # 4. Reload Agent's retriever (lightweight reload)
        print("Refreshing Agent's knowledge base...")
        if tutor_agent:
            tutor_agent.refresh_retriever()
        else:
            tutor_agent = TutorAgent()
        
        return JSONResponse(content={"filename": file.filename, "message": "File uploaded and processed successfully."})
        
    except Exception as e:
        print(f"Error during upload/ingest: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    # For debugging/development
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)
