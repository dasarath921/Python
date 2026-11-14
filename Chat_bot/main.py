
import os
from dotenv import load_dotenv
from google import genai
from reader import load_policies

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL="gemini-3.5-flash-lite"


client = genai.Client(api_key=API_KEY)

# Read all policy files
policies = load_policies()
print(len(policies))

while True:
    question = input("\nAsk a policy question (or type exit): ")

    if question.lower() == "exit":
        break

    prompt = f"""
You are a company policy assistant.

Answer the user's question using ONLY the policy documents below.

Rules:
1. Do not make up policy information.
2. If the answer is not available in the documents, say:
   "This information is not mentioned in the available company policies."
3. Keep the answer simple and clear.
4. Mention the policy filename used for the answer.

COMPANY POLICIES:
{policies}

USER QUESTION:
{question}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        print("\nAnswer:")
        print(response.text)

    except Exception as e:
        print("Error:", e)
