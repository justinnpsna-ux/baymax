import json

def injectMemory(): # this is how ill do it for now. very simple
    with open("memory.json", "r") as file:
        memory = json.load(file) 

    return f"""
    Known information about the user:

    Name: {memory["name"]}
    Hobbies: {", ".join(memory["hobbies"])}
    Projects: {", ".join(memory["projects"])}
    School: {memory["school"]}
"""
#baymax suggests a memory > u approve it (in the future idea)
def save_memory(): #button > flask > save_memory > update memory.JSON 
    return

def load_memory():
    return