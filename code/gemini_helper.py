import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load env file
load_dotenv()

def get_genai_client():
    """
    Initializes and returns a Google GenAI client.
    Expects GEMINI_API_KEY inside environment variables.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in env variables! Please check your .env file.")
    
    return genai.Client(api_key=api_key)

def generate_response(user_input: str, emotion: str, confidence: float) -> str:
    """
    Connects to Gemini model to formulate highly tailored learning guidance.
    """
    try:
        client = get_genai_client()
        
        prompt = f"""
        You are an empathetic learning mentor supporting a student.
        The student feels: {emotion} (Confidence: {confidence}).
        Student's Message: "{user_input}"

        Please provide highly actionable, compassionate, and structured study guidance tailored to this emotional state. 
        - Keep your tone supportive, encouraging, and clear.
        - Provide 2-3 specific learning strategies or mindset tips relevant to their current feeling.
        - Keep the response concise but warm and tailored.
        """
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        
        return response.text
    except Exception as e:
        return f"Hey! I'm here to support you. (AI Error: {e})"