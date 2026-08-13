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