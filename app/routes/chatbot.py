from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.gemini_service import chat_with_gemini
from hyperon import MeTTa
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class KnowledgeUpdate(BaseModel):
    question: str
    answer: str


load_dotenv()
# Initialize MeTTa engine
engine = MeTTa()

knowledge_base = """
(FAQ "What is AI?" "AI stands for Artificial Intelligence, which simulates human intelligence in machines.")
(FAQ "What is ML?" "Machine Learning (ML) is a subset of AI that allows systems to learn from data.")
"""

engine.run(knowledge_base)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Set it in the environment variables.")


genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-1.5-pro-002")

def query_knowledge_graph(question: str) -> str:
    query_result = engine.run(f'!(match &self (FAQ "{question}" $answer) $answer)')

    if query_result:
        result = str(query_result[0]).strip('[]"')
        print(f"Processed result: {repr(result)}")  
        if result and result.strip(): 
            return result
        return generate_rag_response(question)

def generate_rag_response(question: str) -> str:
    """Use Gemini to generate an answer when the knowledge graph has no answer."""
    response = gemini_model.generate_content(question)
    return response.text if response.text else "I couldn't find an answer."


def update_knowledge(question: str, answer: str):
    new_faq = f'(FAQ "{question}" "{answer}")'
    engine.run(new_faq)  

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to the Gemini Chatbot API! 🚀"}



@router.post("/chat")
async def chat(request: QuestionRequest):
    """Endpoint to query the knowledge graph for an answer."""
    response = query_knowledge_graph(request.question)
    if not response:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"response": response}

@router.post("/update_knowledge")
async def update_knowledge_endpoint(data: KnowledgeUpdate):
    """Endpoint to update knowledge in the knowledge graph."""
    update_knowledge(data.question, data.answer)
    return {"message": "Knowledge updated successfully!"}