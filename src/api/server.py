from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent.tutor import TutorAgent
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(title="AI Tutor API", version="1.0.0")

# Request Models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    answer: str

# Global Agent Instance (Lazy loading or immediate)
# We initialize it here so it persists across requests
try:
    tutor_agent = TutorAgent()
    print("AI Tutor Agent initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Tutor Agent: {e}")
    tutor_agent = None

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "healthy", "agent_status": "ready" if tutor_agent else "failed"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint to interact with the AI Tutor.
    """
    if not tutor_agent:
        raise HTTPException(status_code=503, detail="Tutor Agent is not initialized.")
    
    try:
        response = tutor_agent.ask(request.message, session_id=request.session_id)
        return ChatResponse(answer=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # For debugging/development
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)
