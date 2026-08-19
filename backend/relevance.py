from flask import request, jsonify
import json
import requests
from datetime import datetime

def get_keywords(data):

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
                            You are Baymax's memory relevance finding system.

                            Analyze the user's message.

                            Determine whether it contains durable, factual information about the user,
                            the user's goals, dreams and desires, what the user is currently seriously working on,
                            the user's serious opinion about ideas or the people around them, that would 
                            be useful for finding relevance within a potential set of pre-collected memories.

                            If there is a potential need to find relevance, come up with useful keywords 
                            (and 1 last NOUN keyword that generalizes the user's prompt's subject 
                            (for example: is the user talking about a "goal" or a "sport"? if so, include that last keyword))

                            You can leave as many keywords as you think necessary

                            and return ONLY valid JSON in this format:

                            {{
                                "keywords": ["keyword1", "keyword2"] 
                            }}

                            If the user is asking for you to remember a specific detail or if you do remember a specific detail,
                            please come up with at least 1 keyword

                            If the user's message is simply a greeting or a joke, return:

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
        print("***no potential relevance***")
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
                if str(word) in keyword:
                    relevant_info += memory["fact"]
    return relevant_info