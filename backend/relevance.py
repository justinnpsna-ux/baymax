from flask import request, jsonify
import json
import requests
from datetime import datetime

def get_keywords():
    data = request.get_json() 

    if data is None:
        return jsonify({"error": "No valid data received"}), 400

    try:
        memory_obj = requests.post(
                'http://localhost:11434/api/chat',
                json={
                    "model": "qwen3.5:9b",
                    "messages": [ 
                        {
                        "role": "user",
                        "content": f'''
                            You are Baymax's memory extraction system.

                            Analyze the user's message.

                            Determine whether it contains durable, factual information about the user,
                            the user's goals and desires, what the user is currently seriously working on,
                            or the user's serious opinion about ideas that would be useful for finding relevance
                            within a set of pre-collected memories.

                            If there is useful information, return ONLY valid JSON in this format:

                            {{
                                "keywords": ["keyword1", "keyword2"] 
                            }}

                            If there is nothing worth checking for relevance, return:

                            null

                            user's message: {data["prompt"]}
                            '''
                        }],
                    "think": False,
                    "stream": False,
                    "options": {
                    #"num_predict": 500000
                    }
                })
    except json.JSONDecodeError:
        return "error"

    if memory_obj.json()["message"]["content"] == "null":
        return '', 204

    print(json.loads(memory_obj.json()["message"]["content"])["keywords"])
    return json.loads(memory_obj.json()["message"]["content"])["keywords"]

def find_relevance(keywords, fileName):
    relevant_info = ""

    with open(fileName, "r") as file:
            memory_bank = json.load(file)

    for word in keywords:
        for memory in memory_bank:
            for keyword in memory["keywords"]:
                if word == keyword:
                    relevant_info += memory["fact"]
    return relevant_info