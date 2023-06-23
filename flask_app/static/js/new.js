// Get the chat form element
const chatForm = document.getElementById('chat-form');

// Add an event listener for form submission
chatForm.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent the default form submission behavior

    // Get the user input from the input element
    const userInput = document.getElementById('user-input').value;

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Add the user's message to the chat log
    const chatLog = document.getElementById('chat-log');
    chatLog.innerHTML += '<p>You: ' + userInput + '</p>';

    // Send an asynchronous POST request to the Flask route
    fetch(chatForm.action, {
        method: 'POST',
        body: JSON.stringify({ message: userInput }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Add the response from the Flask route to the chat log
        chatLog.innerHTML += '<p>Chatbot: ' + data.reply + '</p>';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
