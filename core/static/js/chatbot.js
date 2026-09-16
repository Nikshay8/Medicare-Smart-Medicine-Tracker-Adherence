document.addEventListener("DOMContentLoaded", function () {
    const fab        = document.getElementById("chatbotFab");
    const win         = document.getElementById("chatbotWindow");
    const closeBtn    = document.getElementById("chatbotClose");
    const messagesBox = document.getElementById("chatbotMessages");
    const input       = document.getElementById("chatbotInput");
    const sendBtn     = document.getElementById("chatbotSendBtn");
    const micBtn      = document.getElementById("chatbotMicBtn");

    if (!fab || !win) return;

    fab.addEventListener("click", function () {
        win.classList.toggle("open");
        if (win.classList.contains("open")) input.focus();
    });
    closeBtn.addEventListener("click", function () {
        win.classList.remove("open");
    });

    function getCsrfToken() {
        const match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? match[1] : "";
    }

    function addMessage(text, type) {
        const row = document.createElement("div");
        row.className = "chatbot-msg-row";

        const bubble = document.createElement("div");
        bubble.className = "chatbot-msg " + type;
        bubble.textContent = text;
        row.appendChild(bubble);

        if (type === "bot" && "speechSynthesis" in window) {
            const speakBtn = document.createElement("button");
            speakBtn.className = "chatbot-speak-btn";
            speakBtn.innerHTML = "🔊";
            speakBtn.title = "Sunein";
            speakBtn.addEventListener("click", function () {
                speakText(text);
            });
            row.appendChild(speakBtn);
        }

        messagesBox.appendChild(row);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function addTypingIndicator() {
        const el = document.createElement("div");
        el.className = "chatbot-typing";
        el.id = "chatbotTyping";
        el.textContent = "Likh raha hoon...";
        messagesBox.appendChild(el);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function removeTypingIndicator() {
        const el = document.getElementById("chatbotTyping");
        if (el) el.remove();
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, "user");
        input.value = "";
        addTypingIndicator();

        try {
            const response = await fetch("/chatbot-reply/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCsrfToken(),
                },
                body: JSON.stringify({ message: text }),
            });

            const data = await response.json();
            removeTypingIndicator();

            if (!response.ok || data.error) {
                addMessage(data.error || "Kuch gadbad ho gayi. Dobara try karein.", "error");
                return;
            }

            addMessage(data.reply, "bot");

        } catch (err) {
            removeTypingIndicator();
            addMessage("Network mein dikkat aa rahi hai. Internet check karein.", "error");
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") sendMessage();
    });

    function speakText(text) {
        try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "hi-IN";
            utterance.rate = 0.9;
            window.speechSynthesis.speak(utterance);
        } catch (err) {
            console.warn("Text-to-speech not available:", err);
        }
    }

    const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isRecording = false;

    if (SpeechRecognitionAPI) {
        recognition = new SpeechRecognitionAPI();
        recognition.lang = "hi-IN";
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function () {
            isRecording = true;
            micBtn.classList.add("recording");
        };

        recognition.onend = function () {
            isRecording = false;
            micBtn.classList.remove("recording");
        };

        recognition.onerror = function (event) {
            isRecording = false;
            micBtn.classList.remove("recording");
            if (event.error === "not-allowed" || event.error === "permission-denied") {
                addMessage("Mic ki permission nahi mili. Browser settings mein mic allow karein.", "error");
            } else {
                addMessage("Awaaz samajh nahi aayi. Dobara try karein.", "error");
            }
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            input.value = transcript;
            sendMessage();
        };

        micBtn.addEventListener("click", function () {
            if (isRecording) {
                recognition.stop();
            } else {
                try {
                    recognition.start();
                } catch (err) {
                    console.warn("Could not start recognition:", err);
                }
            }
        });
    } else {
        micBtn.addEventListener("click", function () {
            addMessage("Is browser mein voice input available nahi hai. Chrome try karein.", "error");
        });
        micBtn.style.opacity = "0.5";
    }
});