document.querySelector('#chatForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const chatContainer = document.getElementById('chatContainer')
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (message === '') return;

    appendMessage('user', message);

    messageInput.value = '';

    try {
        const response = await axios.post(postUrl ,{ message }, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content,
            }
        });
        appendMessage('assistant', response.data.botResponse);
    } catch (error) {
        appendMessage('assistant', 'Something went wrong, Please try again');
    }
    
    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        const senderClass = sender === 'user' ? 'self-end border-blue-500' : 'self-start border-gray-500'

        messageElement.className = `border ${senderClass} flex p-3 max-w-[70%] shadow-md`

        messageElement.innerHTML += `
                <div>User :</div>
                <div>${message}</div>
            `
        chatContainer.appendChild(messageElement)
        chatContainer.scrollTop = chatContainer.scrollHeight
    }

});
