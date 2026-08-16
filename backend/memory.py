from flask import request
import json

def injectMemory(): # this is how ill do it for now. very simple
    with open("backend/memory.json", "r") as file:
        memory = json.load(file) 

        user_info = "Known information about the user: "

        for key, value in memory.items():
            if isinstance(value, list):
                user_info += f"\n{key}: {", ".join(value)}"
            else:
                user_info += f"\n{key}: {value}"   
        return user_info

#baymax suggests a memory > u approve it (in the future idea)
def save_memory(): #button > flask > save_memory > update memory.JSON 
    data = request.get_json()
    keyword = data["key"]
    desc = data["value"]
    with open("backend/memory.json", "r") as file:
        memory = json.load(file)

    if memory[keyword]:
        memory[keyword] = [memory[keyword], desc]
    else:
        memory[keyword] = desc

    with open("backend/memory.json", "w") as file:
        json.dump(memory, file, indent=4)  

    return "", 204

def load_memory():
    with open("backend/memory.json", "r") as file:
        memory = json.load(file)
    return memory