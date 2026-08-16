import { textToSpeech } from "./index.js";

const memoryKey = document.getElementById('userInput-memory-update-key');
const memoryValue = document.getElementById('userInput-memory-update-value');

const enterBtn = document.getElementById('enterBtn-memory-update');

let currentUtterance; 

async function updateMemory(memoryKey, memoryValue) {

    window.speechSynthesis.cancel(); //it cuts off idk
    currentUtterance = new SpeechSynthesisUtterance("memory updated");
    window.speechSynthesis.speak(currentUtterance);

    try {
        const response = await fetch('http://localhost:8080/api/memory', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            key: memoryKey,
            value: memoryValue
        })
    });

    } catch (error) {
        console.error("Could not connect to the backend:", error);
    }
}

enterBtn.addEventListener('click', async () => {
    try {
        await updateMemory(memoryKey.value, memoryValue.value)
    } catch (error) {
        console.error("Could not use memory key or value", error);
    }
})