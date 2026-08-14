import { getResponse } from "./index.js";

const keysPressed = {
    ShiftRight: false
}

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;
recognition.maxAlternatives = 1;

recognition.onstart = () => {
    console.log("🎤 Listening...");
};

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;

    getResponse(transcript);
    console.log("You said:", transcript);
};

recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
};

recognition.onend = () => {
    console.log("🛑 Done listening.");
};

function importTranscript(transcript) {
    return transcript;
}

window.addEventListener('keydown', (event) => {
    if (event.code in keysPressed) {
        keysPressed[event.code] = true; // ill use hold to talk in the future. dont mind this for now
        recognition.start();
    }
});

window.addEventListener('keyup', (event) => {
    if (event.code in keysPressed) {
        keysPressed[event.code] = false;
    }
});