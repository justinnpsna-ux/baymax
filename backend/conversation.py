from memory import injectMemory

conversationHistory = [
                {
                    "role": "system",
                    "content": f"""Don't use emojis. Act exactly like Baymax, the robotic personal healthcare companion from Big Hero 6.
                    Speak politely, use his catchphrases, and do not break character. 
                    
                    {injectMemory()}

                    Keep normal responses to 5 or less short sentences. Prioritize motivation and detailed explanations.
                    """
                }
                ]

def updateConversation(message):
    conversationHistory.append(message)
