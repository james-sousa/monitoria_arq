// Elementos do DOM
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const chatForm = document.getElementById('chatForm');

// Estado
let apiReady = false;

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    checkApiHealth();
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && apiReady) {
            handleSendMessage(e);
        }
    });
});

// Verificar saúde da API
async function checkApiHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'ok') {
            if (data.api_configured) {
                setStatusOnline();
                messageInput.disabled = false;
                sendBtn.disabled = false;
                apiReady = true;
            } else {
                setStatusOffline('API key não configurada');
                showSystemMessage('Erro: GROQ_API_KEY não está configurada. Configure a variável de ambiente.');
            }
        } else {
            setStatusOffline('Servidor indisponível');
        }
    } catch (error) {
        setStatusOffline('Conexão falhou');
        showSystemMessage('Erro: Não foi possível conectar ao servidor. Certifique-se que o backend está rodando em http://localhost:5000');
        console.error('Erro ao verificar saúde da API:', error);
    }
}

// Atualizar status
function setStatusOnline() {
    statusDot.classList.add('online');
    statusDot.classList.remove('offline');
    statusText.textContent = 'Online';
}

function setStatusOffline(message) {
    statusDot.classList.add('offline');
    statusDot.classList.remove('online');
    statusText.textContent = message || 'Offline';
    apiReady = false;
    messageInput.disabled = true;
    sendBtn.disabled = true;
}

// Enviar mensagem
async function handleSendMessage(event) {
    event.preventDefault();
    
    const message = messageInput.value.trim();
    
    if (!message || !apiReady) {
        return;
    }
    
    // Limpar input
    messageInput.value = '';
    
    // Adicionar mensagem do usuário
    addMessage(message, 'user');
    
    // Desabilitar input durante processamento
    messageInput.disabled = true;
    sendBtn.disabled = true;
    
    // Mostrar loading
    const loadingId = showLoading();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // Remover loading
        removeMessage(loadingId);
        
        if (response.ok && data.success) {
            // Adicionar resposta do assistente
            addMessage(data.response, 'assistant');
        } else {
            // Mostrar erro
            const errorMsg = data.error || 'Erro ao processar a mensagem';
            addMessage(`${errorMsg}`, 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        removeMessage(loadingId);
        addMessage(`Erro de conexão: ${error.message}`, 'error');
    } finally {
        // Reabilitar input
        messageInput.disabled = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

// Adicionar mensagem ao chat
function addMessage(content, type = 'assistant') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Se for markdown ou contém formatação, renderizar com quebras de linha
    if (type === 'assistant' || type === 'error') {
        contentDiv.innerHTML = escapeHtml(content)
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/__(.*?)__/g, '<u>$1</u>');
    } else {
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll para o final
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv.id = 'msg-' + Date.now();
}

// Mostrar loading
function showLoading() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant loading';
    const id = 'loading-' + Date.now();
    messageDiv.id = id;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll para o final
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return id;
}

// Remover mensagem
function removeMessage(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

// Mostrar mensagem do sistema
function showSystemMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = message;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll para o final
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
