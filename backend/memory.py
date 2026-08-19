from flask import request, jsonify
import json
import requests
from datetime import datetime

def injectMemory(): # this is how ill do it for now. very simple
    with open("backend/memory.json", "r") as file:
        memory = json.load(file) 

        user_info = "Known information about the user: "

        for key, value in memory.items():
            if isinstance(value, list):
                user_info += f"\n{key}: {', '.join(value)}"
            else:
                user_info += f"\n{key}: {value}"   
        return user_info

#baymax suggests a memory > u approve it (in the future idea)
def save_memory(fileName, data): #button > flask > save_memory > update memory.JSON 
    keyword = data["key"]
    desc = data["value"]

    if not keyword or not desc:
        return "", 204

    with open(fileName, "r") as file:
        memory = json.load(file)

    if keyword in memory:
        memory[keyword] = [memory[keyword], desc]
    else:
        memory[keyword] = desc

    with open(fileName, "w") as file:
        json.dump(memory, file, indent=4)  

    return "", 204

def load_memory(arr):
    arr[0] =  {
                "role": "system",
                "content": f"""Don't use emojis. Act exactly like Baymax, the robotic personal healthcare companion from Big Hero 6.
                Speak politely, use his catchphrases, and do not break character. 
                    
                {injectMemory()}
    
                Keep normal responses to 5 or less short sentences. Prioritize motivation and detailed explanations.
                """
            }
    return '', 204

def extract_memory(data):

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
                            or the user's serious opinion about ideas or the people around them that would 
                            be useful in future conversations.

                            Do NOT store greetings, jokes, or information that is
                            only relevant to the current conversation.

                            If there is useful information, return ONLY valid JSON in this format:

                            {{
                                "keywords": ["keyword1", "keyword2", "NOUN keyword"], 
                                "fact": "One concise factual sentence about the user within their particular message.", 
                                "type": "temporary OR persistent. (choose one depending on if this information would only be relevant in the near future or also in the far future)"
                            }}

                            Please include 1 last NOUN keyword that generalizes the user's prompt's subject 
                            (for example: is the user talking about a "goal" or a "sport"? if so, include that last keyword)

                            You can leave as many keywords as you think necessary

                            If there is nothing worth remembering, return:

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
    
    save_longTerm_memory("backend/longTerm_memory.json", json.loads(memory_obj.json()["message"]["content"]))
    return '', 204

def save_longTerm_memory(fileName, data): 
    timestamp = datetime.now().isoformat()

    with open(fileName, "r") as file:
        memory = json.load(file)

    data["timestamp"] = timestamp
    memory.append(data)

    with open(fileName, "w") as file:
        json.dump(memory, file, indent=4)  
    
    return "", 204