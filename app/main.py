from fastapi import FastAPI
from app.routes.chatbot import router as chatbot_router

# Initialize the FastAPI app
app = FastAPI()

# Include the chatbot router
app.include_router(chatbot_router)
