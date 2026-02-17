// static/js/chat.js
// Lógica do chatbot

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');
    const sugestoesGrid = document.getElementById('sugestoes-grid');

    // Carregar sugestões ao iniciar
    carregarSugestoes();

    // Event listeners
    sendButton.addEventListener('click', enviarMensagem);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') enviarMensagem();
    });

    // Função para carregar sugestões da API
    function carregarSugestoes() {
        fetch('/api/chat/sugestoes')
            .then(response => response.json())
            .then(data => {
                data.sugestoes.forEach(sugestao => {
                    const item = document.createElement('div');
                    item.className = 'sugestao-item';
                    item.textContent = sugestao;
                    item.onclick = () => {
                        userInput.value = sugestao;
                        enviarMensagem();
                    };
                    sugestoesGrid.appendChild(item);
                });
            })
            .catch(error => console.error('Erro ao carregar sugestões:', error));
    }

    // Função para enviar mensagem
    function enviarMensagem() {
        const pergunta = userInput.value.trim();
        if (!pergunta) return;

        // Adiciona mensagem do usuário
        adicionarMensagem('user', pergunta);
        userInput.value = '';

        // Mostra indicador de digitação
        typingIndicator.style.display = 'block';
        sendButton.disabled = true;
        userInput.disabled = true;

        // Envia para o backend
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ pergunta: pergunta })
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.style.display = 'none';
            adicionarMensagem('bot', data.resposta);
        })
        .catch(error => {
            typingIndicator.style.display = 'none';
            adicionarMensagem('bot', 'Desculpe, tive um problema. Pode tentar novamente?');
            console.error('Erro:', error);
        })
        .finally(() => {
            sendButton.disabled = false;
            userInput.disabled = false;
            userInput.focus();
        });
    }

    // Função para adicionar mensagem ao chat
    function adicionarMensagem(tipo, conteudo) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${tipo}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Converte markdown simples para HTML
        let htmlConteudo = conteudo
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
        
        contentDiv.innerHTML = htmlConteudo;
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Rola para a última mensagem
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});