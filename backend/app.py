from flask import Flask, Response, request, jsonify
from flask_cors import CORS 
import requests
import json

from conversation import updateConversation, conversationHistory
from memory import save_memory, load_memory

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

    def generate_stream():
        ollama_response = requests.post(
            'http://localhost:11434/api/chat',
            json={
                "model": "qwen3.5:9b",
                "messages": conversationHistory,
                "think": False,
                "stream": True,
                "options": {
                #"num_predict": 500000
            }
            })

        full_response = ""

        for line in ollama_response.iter_lines(chunk_size=1):
            if line:
                decoded_line = line.decode("utf-8")

                try:
                    dataObj = json.loads(decoded_line)
                    dataMessage = dataObj["message"]
                    text_chunk = dataMessage.get("content", "")

                    if text_chunk:
                        full_response += text_chunk
                        yield text_chunk
            
                except json.JSONDecodeError:
                    print(f"Skipping malformed or incomplete chunk: {decoded_line}")
                    continue
        
        updateConversation({"role": "assistant", "content": full_response})
        full_response = ""

    return Response(
        generate_stream(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

@app.route('/api/memory', methods=['POST'])
def update_memory():
    data = request.get_json() 
    
    if data is None:
        return jsonify({"error": "No valid data received"}), 400
    
    save_memory()
    load_memory(conversationHistory)
    return '', 204

def extract_memory():
    data = request.get_json() 

    if data is None:
        return jsonify({"error": "No valid data received"}), 400

    memory_obj = requests.post(
            'http://localhost:11434/api/chat',
            json={
                "model": "qwen3.5:9b",
                "messages": {
                    "role": "user",
                    "content": f"""
                        You are Baymax's memory extraction system.

                        Analyze the user's message.

                        Determine whether it contains durable, factual information about the user
                        that would be useful in future conversations.

                        Do NOT store temporary emotions, greetings, jokes, or information that is
                        only relevant to the current conversation.

                        If there is useful information, return ONLY valid JSON in this format:

                        {
                        "keywords": ["keyword1", "keyword2"],
                        "fact": "One concise factual sentence about the user within their particular message."
                        }

                        If there is nothing worth remembering, return:

                        null

                        user's message: {data["prompt"]}
                        """
                    },
                "think": False,
                "stream": False,
                "options": {
                #"num_predict": 500000
                }
            })

    memory_obj #this needs to go into longMemory.json
    return '', 204

if __name__ == '__main__':
    app.run(port=8080, debug=True)