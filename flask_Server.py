from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        # Call Groq API
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": user_message}]
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            bot_response = response.json()["choices"][0]["message"]["content"]
            return jsonify({"reply": bot_response})
        else:
            return jsonify({"error": f"API error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)