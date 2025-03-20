from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.gemini_service import chat_with_gemini

# Create the APIRouter instance
router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to the Gemini Chatbot API! 🚀"}

# Define the POST route
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chat_with_gemini(request.message)
    return {"response": response}
