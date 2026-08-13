from memory import injectMemory

conversationHistory = [
                {
                    "role": "system",
                    "content": f"""You are Baymax, a friendly conversational companion. 
                    
                    {injectMemory()}

                    Keep normal responses to 1-5 short sentences. Prioritize natural conversation over detailed explanations.
                    """
                }
                ]

def updateConversation(message):
    conversationHistory.append(message)