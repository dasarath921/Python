from dotenv import load_dotenv
from google import genai 
import os;
from pydantic import BaseModel

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

class ChatResponse(BaseModel):
    answer: str
    topic: str
    key_points: list[str]

conversation_history = []
client = genai.Client(api_key=API_KEY)
MODEL="gemini-3.5-flash-lite"


def chat(user_message):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    else:
        try:
            conversation_history.append({"role": "user", "parts": [{"text": user_message}]})
            response = client.models.generate_content(
                model=MODEL,
                contents=conversation_history,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ChatResponse   
                }
            )        
        except:
            raise ValueError("Failed to create a client with the provided API key.")

        conversation_history.append({"role": "model", "parts": [{"text": response.text}]})
        return response.text


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = chat(user_input)
    print("Bot:", response)

