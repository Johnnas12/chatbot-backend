import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Load environment variable (API Key)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def chat_with_gemini(message: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-002")
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return f"Error: {e}"
