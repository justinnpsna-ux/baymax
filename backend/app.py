from flask import Flask, request, jsonify
from flask_cors import CORS 
import requests

from conversation import updateConversation, conversationHistory

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def get_data():
    data = request.get_json() 

    if data is None:
        return jsonify({"error": "No valid data received"}), 400

    updateConversation(
            {
                "role": "user",
                "content": data["prompt"]
            })
    
    ollama_response = requests.post(
        'http://localhost:11434/api/chat',
        json={
            "model": "qwen3:8b",
            "messages": conversationHistory,
            "think": False,
            "stream": False,
            "options": {
            "num_predict": 200
        }
        }
    )
    
    updateConversation(ollama_response.json()["message"])

    return jsonify(ollama_response.json())

if __name__ == '__main__':
    app.run(port=8000, debug=True)