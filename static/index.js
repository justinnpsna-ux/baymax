

const userInput = document.getElementById('userInput');
const ollamaOutput = document.getElementById('ollama_response')

const enterBtn = document.getElementById('enterBtn');

export async function getResponse(userPrompt) {
    let fullResponseText = ""; 

    try {
        ollamaOutput.textContent = "";
        const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: userPrompt
        })
    });

        //const data = await response.json();

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
    
        let isDone = false;

        while (!isDone) {
            const { value, done } = await reader.read();
      
        if (done) {
            isDone = true;
            break; 
        }

        const textChunk = decoder.decode(value, { stream: true });
        fullResponseText += textChunk;

        console.log(textChunk);
        ollamaOutput.textContent += textChunk;

        await new Promise(resolve => setTimeout(resolve, 0));

        }

    } catch (error) {
        console.error("Could not connect to the backend:", error);
    }

    textToSpeech(fullResponseText)

    fullResponseText = ""
}

function textToSpeech(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.1;
    utterance.pitch = 0.9;
    utterance.pitchMultiplier = 1.0
    utterance.volume = 1.0;
    speechSynthesis.speak(utterance);
}

enterBtn.addEventListener('click', async () => {
    try {
        await getResponse(userInput.value)
    } catch (error) {
        console.error("Could not use prompt", error);
    }
})

//getResponse('hi how are you doing?')
