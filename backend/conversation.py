conversationHistory = [
                {
                    "role": "system",
                    "content": "You are Baymax, a friendly conversational companion. Keep normal responses to 1-5 short sentences. Prioritize natural conversation over detailed explanations."
                }
                ]

def updateConversation(message):
    conversationHistory.append(message)