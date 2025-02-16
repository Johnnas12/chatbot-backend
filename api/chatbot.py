from fastapi import APIRouter
from app.models import ChatRequest, ChatResponse
from app.services.gemini_service import chat_with_gemini

# Create the APIRouter instance
router = APIRouter()

# Define the POST route
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chat_with_gemini(request.message)
    return {"response": response}
