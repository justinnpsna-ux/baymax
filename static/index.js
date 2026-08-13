const userInput = document.getElementById('userInput');
const ollamaOutput = document.getElementById('ollama_response')

const enterBtn = document.getElementById('enterBtn');

async function getResponse(userPrompt) {
    try {
        ollamaOutput.textContent = "thinking...";
        const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: userPrompt
        })
    });

        const data = await response.json();

        console.log(data);
        ollamaOutput.textContent = data.message.content;
        const utterance = new SpeechSynthesisUtterance(data.message.content);
        utterance.rate = 0.75;
        utterance.pitch = 0.9;
        utterance.volume = 1.0;
        speechSynthesis.speak(utterance);

    } catch (error) {
        console.error("Could not connect to the backend:", error);
    }
}

enterBtn.addEventListener('click', async () => {
    try {
        await getResponse(userInput.value)
    } catch (error) {
        console.error("Could not use prompt", error);
    }
})

//getResponse('hi how are you doing?')
