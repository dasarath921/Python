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

def conversation_history_store_in_file():   
    with open("conversation_history.txt", "w") as file:
        for message in conversation_history:
            role = message["role"]
            parts = message["parts"]
            for part in parts:
                text = part["text"]
                file.write(f"{role}: {text}\n")


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
        conversation_history_store_in_file()
        return response.text


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = chat(user_input)
    print("Bot:", response)

