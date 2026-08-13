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