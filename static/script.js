// chatbot_flask/static/script.js

const chatLog = document.getElementById('chatLog');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

function displayMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender + '-message');
    messageDiv.textContent = text;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendMessage() {
    const userText = userInput.value.trim();
    if (userText === "") return;

    displayMessage(userText, 'user');
    userInput.value = "";

    // 1. CRIAR E MOSTRAR O INDICADOR DE "DIGITANDO..." COM PONTINHOS
    // Documentação: Criamos o elemento 'div' para o indicador.
    const typingIndicator = document.createElement('div');
    // Adicionamos as classes 'message' e 'bot-message' para que ele se pareça com um balão de chat do bot.
    // Adicionamos 'typing-indicator' para aplicar os estilos específicos do container dos pontinhos.
    typingIndicator.classList.add('message', 'bot-message', 'typing-indicator');
    typingIndicator.id = 'typingIndicator'; // ID para facilitar a remoção.
    
    // Definimos o HTML interno para criar os três pontinhos.
    typingIndicator.innerHTML = `
        <div class="typing-indicator-dots">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
    `;
    chatLog.appendChild(typingIndicator); // Adiciona o indicador ao chat.
    chatLog.scrollTop = chatLog.scrollHeight; // Rola para mostrar o indicador.

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userText }),
        });

        // 2. REMOVER O INDICADOR DE "DIGITANDO..."
        const indicatorToRemove = document.getElementById('typingIndicator');
        if (indicatorToRemove) {
            chatLog.removeChild(indicatorToRemove);
        }

        if (!response.ok) {
            console.error('Erro do servidor:', response.status, response.statusText);
            const errorData = await response.json().catch(() => ({ reply: "Ocorreu um erro ao contatar o servidor." }));
            displayMessage(`Erro do servidor: ${errorData.reply || response.statusText}`, 'bot');
            return;
        }

        const data = await response.json();
        const botText = data.reply;
        
        // 3. MOSTRAR A RESPOSTA REAL DO BOT
        displayMessage(botText, 'bot');

    } catch (error) {
        // 4. REMOVER O INDICADOR DE "DIGITANDO..." EM CASO DE ERRO DE REDE
        const indicatorToRemoveOnError = document.getElementById('typingIndicator');
        if (indicatorToRemoveOnError) {
            chatLog.removeChild(indicatorToRemoveOnError);
        }
        console.error('Erro ao enviar mensagem:', error);
        displayMessage('Não foi possível conectar ao servidor. Verifique sua conexão ou tente mais tarde.', 'bot');
    }
}

if (sendButton) {
    sendButton.addEventListener('click', sendMessage);
}

if (userInput) {
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
}