from flask import Flask, request, jsonify
from flask_cors import CORS 
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def get_data():
    data = request.get_json() 

    if data is None:
        return jsonify({"error": "No valid data received"}), 400

    ollama_response = requests.post(
        'http://localhost:11434/api/chat',
        json={
            "model": "qwen3:8b",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Baymax, a friendly conversational companion. Keep normal responses to 1-3 short sentences. Prioritize natural conversation over detailed explanations."
                },
                {
                    "role": "user",
                    "content": data["prompt"]
                }
            ],
            "think": False,
            "stream": False,
            "options": {
            "num_predict": 200
        }
        }
    )
    return jsonify(ollama_response.json())

if __name__ == '__main__':
    app.run(port=8000, debug=True)