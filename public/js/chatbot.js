const chatContainer = document.getElementById('chatContainer');
const sendButton = document.getElementById('sendButton');
const sendIcon = document.getElementById('sendIcon');
const messageInput = document.getElementById('messageInput');

messageInput.addEventListener('input', function() {
    const message = messageInput.value.trim();
    
    message.length > 0
    ? sendButton.disabled = false
    : sendButton.disabled = true;
});

document.querySelector('#chatForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const message = messageInput.value.trim();
    
    if (message === '') return;
    
    appendMessage('user', message);
    
    messageInput.value = '';

    sendButton.disabled = false;
    
    sendIcon.textContent = '↻';
    
    try {
        const response = await axios.post(postUrl ,{'message': message}, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content,
            }
        });
        console.log(response.data);
        appendMessage('assistant', response.data.generation, response.data.mood);
    } catch (error) {
        console.log(error);
        appendMessage('assistant', `Something went wrong, Please try again. Error: ${error.message}`);
    }
    
    function appendMessage(sender, message, assistant_mood = null) {
        const messageElement = document.createElement('div');
        const senderClass = sender === 'user' ? 'self-end justify-end' : 'self-start justify-start'
        
        messageElement.className = `${senderClass} p-3 flex`
        
        if (sender === 'user') {
            messageElement.innerHTML += `
                            <div class="justify-end p-3 flex">
                                <p class="bg-gray-200 text-slate-950 rounded-xl p-3 mx-2 max-w-[80%] break-words break-all">${message}</p>
                                <div class="border border-black w-14 h-14 flex rounded-full">
                                    <img src="" class="text-md m-auto" alt="User Profile">
                                </div>
                            </div>
            `
        } else {
            messageElement.innerHTML += `
                            <div class="justify-start p-3 flex">
                                <div class="w-14 h-14 flex rounded-full">
                                    <img src="images/${assistant_mood}.png" class="text-md m-auto" alt="Bot Profile">
                                </div>
                                <p class="bg-slate-800 text-slate-200 rounded-xl p-3 mx-2 max-w-[80%] break-words break-all">${message}</p>
                            </div>
            `
        }
        chatContainer.appendChild(messageElement)
        chatContainer.scrollTop = chatContainer.scrollHeight
        
        sendButton.disabled = true;
        sendIcon.textContent = '↑';
    }
    
});

document.getElementById('closeError').addEventListener('click', function() {
    const overlay = document.getElementById('errorOverlay');
    const errorBox = document.getElementById('errorBox');
    
    if (overlay) overlay.style.display = 'none';
    if (errorBox) errorBox.style.display = 'none';
});
