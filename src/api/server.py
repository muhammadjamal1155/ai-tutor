from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.agent.tutor import TutorAgent
from src.ingest import ingest_data
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

class ChatResponse(BaseModel):
    answer: str

@app.on_event("startup")
async def startup_event():
    global tutor_agent, init_error
    from src.config.settings import config
    print(f"Server Startup. Using Key: {config.GOOGLE_API_KEY[:10]}...", flush=True)
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
    """
    global tutor_agent
    
    if not tutor_agent:
        # Try one more time (lazy load) if it failed before? No, simpler to just report error.
        detail_msg = f"Tutor Agent is not initialized. Error: {init_error}"
        raise HTTPException(status_code=503, detail=detail_msg)
    
    try:
        response = tutor_agent.ask(request.message, session_id=request.session_id)
        return ChatResponse(answer=response)
    except Exception as e:
        print(f"Error processing chat request: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF file, save it, and re-run ingestion.
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
        
        # 3. Release Locks & Trigger Ingestion
        print("Releasing locks before ingestion...")
        global tutor_agent
        tutor_agent = None 
        import gc
        gc.collect()
        
        print("Triggering ingestion...")
        ingest_data() 
        
        # 4. Reload Agent
        print("Reloading Agent with new knowledge...")
        tutor_agent = TutorAgent()
        
        return JSONResponse(content={"filename": file.filename, "message": "File uploaded and processed successfully. You can now chat regarding this document."})
        
    except Exception as e:
        print(f"Error during upload/ingest: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    # For debugging/development
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)
