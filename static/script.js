
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("clear-btn").addEventListener("click", clearChat); 

function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    // Display user message
    const chatHistory = document.getElementById("chat-history");
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.innerText = userInput;
    chatHistory.appendChild(userMessage);

    // Send query to the server
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.innerText = data.response;
        chatHistory.appendChild(botMessage);

        // Scroll to the bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
    });

    // Clear input field
    document.getElementById("user-input").value = "";
}

function clearChat() {
    // Clear the chat history
    const chatHistory = document.getElementById("chat-history");
    chatHistory.innerHTML = "";

    // Clear the input field
    document.getElementById("user-input").value = "";
}
    