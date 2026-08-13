import json

with open("memory.json", "r") as file:
    memory = json.load(file)

memory_context = f"""
    Known information about the user:

    Name: {memory["name"]}
    Hobbies: {", ".join(memory["hobbies"])}
    Projects: {", ".join(memory["projects"])}
    School: {memory["school"]}
"""

def injectMemory(): # this is how ill do it for now. very simple
    return memory_context