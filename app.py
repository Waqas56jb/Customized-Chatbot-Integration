import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Groq API key from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Ensure the API key is loaded
if not GROQ_API_KEY:
    raise ValueError("API key not found. Please ensure the .env file is correctly set.")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def chat_with_groq(message):
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Chat loop
print("Groq Chatbot (type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    reply = chat_with_groq(user_input)
    print("Bot:", reply)
