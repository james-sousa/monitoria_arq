// ── Estado ────────────────────────────────────────────────────────────────────
const SESSION_KEY = 'comparch_session_id';

let sessionId   = localStorage.getItem(SESSION_KEY) || generateId();
let apiReady    = false;
let isWaiting   = false;

localStorage.setItem(SESSION_KEY, sessionId);

// ── DOM ───────────────────────────────────────────────────────────────────────
const messagesEl = document.getElementById('messages');
const msgInput   = document.getElementById('msgInput');
const sendBtn    = document.getElementById('sendBtn');
const statusDot  = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const topbarModel= document.getElementById('topbarModel');

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    setupInput();
});

function setupInput() {
    msgInput.addEventListener('input', () => {
        // Auto-resize textarea
        msgInput.style.height = 'auto';
        msgInput.style.height = Math.min(msgInput.scrollHeight, 160) + 'px';
    });

    msgInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (apiReady && !isWaiting) sendMessage();
        }
    });
}

// ── Health check ──────────────────────────────────────────────────────────────
async function checkHealth() {
    try {
        const res  = await fetch('/api/health');
        const data = await res.json();

        if (data.status === 'ok' && data.api_configured) {
            setOnline();
            topbarModel.textContent = data.model || '';
        } else {
            setOffline('API key ausente');
            appendSystem('Configure a variável <code>OPENROUTER_API_KEY</code> no servidor e reinicie.');
        }
    } catch {
        setOffline('Servidor offline');
        appendSystem('Não foi possível conectar ao backend. Certifique-se de que está rodando em <code>localhost:5000</code>.');
    }
}

function setOnline() {
    statusDot.className  = 'status-dot online';
    statusText.textContent = 'Online';
    apiReady = true;
    msgInput.disabled = false;
    sendBtn.disabled  = false;
    msgInput.focus();
}

function setOffline(msg) {
    statusDot.className    = 'status-dot offline';
    statusText.textContent = msg;
    apiReady  = false;
    msgInput.disabled = true;
    sendBtn.disabled  = true;
}

// ── Enviar mensagem ───────────────────────────────────────────────────────────
async function sendMessage() {
    const text = msgInput.value.trim();
    if (!text || !apiReady || isWaiting) return;

    // Limpa boas-vindas
    document.querySelector('.welcome')?.remove();

    // Mostra mensagem do usuário
    appendBubble(text, 'user');

    // Reset input
    msgInput.value = '';
    msgInput.style.height = 'auto';

    // Loading state
    isWaiting = true;
    sendBtn.disabled = true;
    const loadingId = showLoading();

    try {
        const res  = await fetch('/api/chat', {
            method : 'POST',
            headers: { 'Content-Type': 'application/json' },
            body   : JSON.stringify({ message: text, session_id: sessionId }),
        });

        const data = await res.json();
        removeEl(loadingId);

        if (res.ok && data.success) {
            appendAssistant(data.response, data.tool_calls || []);
        } else {
            appendBubble(data.error || 'Erro desconhecido.', 'error');
        }
    } catch (err) {
        removeEl(loadingId);
        appendBubble('Erro de conexão: ' + err.message, 'error');
    } finally {
        isWaiting = false;
        sendBtn.disabled = false;
        msgInput.focus();
    }
}

// ── Renderizadores ────────────────────────────────────────────────────────────

/** Bolha simples (user / error) */
function appendBubble(text, type) {
    const row = document.createElement('div');
    row.className = `msg-row ${type}`;

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = type === 'user' ? '🧑' : '✕';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.textContent = text;

    row.append(avatar, bubble);
    messagesEl.appendChild(row);
    scrollBottom();
}

/** Resposta completa do assistente com tool calls + markdown + PDF card */
function appendAssistant(text, toolCalls) {
    const row = document.createElement('div');
    row.className = 'msg-row assistant';

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = '⬡';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';

    // Tool calls badges
    if (toolCalls.length > 0) {
        const tc = document.createElement('div');
        tc.className = 'tool-calls';
        toolCalls.forEach(t => {
            try {
                const obj  = JSON.parse(t.chamada);
                const badge = document.createElement('div');
                badge.className = 'tool-badge';
                badge.innerHTML = `<span class="tool-badge-icon">⚙</span>
                                   <span class="tool-badge-name">${escHtml(obj.tool)}</span>
                                   <span>executada</span>`;
                tc.appendChild(badge);
            } catch { /* chamada não é JSON válido, ignora */ }
        });
        bubble.appendChild(tc);
    }

    // Markdown
    const content = document.createElement('div');
    content.innerHTML = renderMarkdown(text);
    bubble.appendChild(content);

    // PDF card — detecta caminho de arquivo retornado pelo agente
    const pdfMatch = text.match(/Arquivo:\s*([^\n]+\.pdf)/);
    if (pdfMatch) {
        const caminho = pdfMatch[1].trim();
        const nome    = caminho.split('/').pop();
        bubble.appendChild(buildPdfCard(nome, caminho));
    }

    row.append(avatar, bubble);
    messagesEl.appendChild(row);
    scrollBottom();
}

function appendSystem(html) {
    const div = document.createElement('div');
    div.style.cssText = 'text-align:center;padding:12px;font-size:12px;color:var(--text3)';
    div.innerHTML = html;
    messagesEl.appendChild(div);
    scrollBottom();
}

// ── PDF card ──────────────────────────────────────────────────────────────────
function buildPdfCard(nome, caminho) {
    const card = document.createElement('a');
    card.className = 'pdf-card';
    card.href      = `/api/pdf/${encodeURIComponent(nome)}`;
    card.target    = '_blank';
    card.rel       = 'noopener';
    card.innerHTML = `
        <span class="pdf-card-icon">📄</span>
        <div class="pdf-card-info">
            <div class="pdf-card-title">${escHtml(nome)}</div>
            <div class="pdf-card-sub">${escHtml(caminho)}</div>
        </div>
        <button class="pdf-card-btn" onclick="event.preventDefault(); window.open(this.closest('a').href)">
            Baixar
        </button>`;
    return card;
}

// ── Markdown renderer (leve, sem dependências) ────────────────────────────────
function renderMarkdown(raw) {
    let s = escHtml(raw);

    // Blocos de código
    s = s.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) =>
        `<pre><code class="lang-${escHtml(lang)}">${code.trimEnd()}</code></pre>`);

    // Código inline
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Headings
    s = s.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    s = s.replace(/^## (.+)$/gm,  '<h2>$1</h2>');
    s = s.replace(/^# (.+)$/gm,   '<h1>$1</h1>');

    // Bold / italic
    s = s.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    s = s.replace(/\*\*(.+?)\*\*/g,     '<strong>$1</strong>');
    s = s.replace(/\*(.+?)\*/g,         '<em>$1</em>');

    // Blockquote
    s = s.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');

    // Tabela markdown
    s = s.replace(/\|(.+)\|\n\|[-| :]+\|\n((?:\|.+\|\n?)+)/g, (_, header, body) => {
        const ths = header.split('|').filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join('');
        const rows = body.trim().split('\n').map(row => {
            const tds = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
            return `<tr>${tds}</tr>`;
        }).join('');
        return `<table><thead><tr>${ths}</tr></thead><tbody>${rows}</tbody></table>`;
    });

    // Listas não-ordenadas
    s = s.replace(/((?:^[-*] .+\n?)+)/gm, block => {
        const items = block.trim().split('\n')
            .map(l => `<li>${l.replace(/^[-*] /, '')}</li>`).join('');
        return `<ul>${items}</ul>`;
    });

    // Listas ordenadas
    s = s.replace(/((?:^\d+\. .+\n?)+)/gm, block => {
        const items = block.trim().split('\n')
            .map(l => `<li>${l.replace(/^\d+\. /, '')}</li>`).join('');
        return `<ol>${items}</ol>`;
    });

    // Parágrafos (linhas duplas)
    s = s.split(/\n{2,}/).map(p => {
        p = p.trim();
        if (!p) return '';
        if (/^<(h[1-3]|ul|ol|pre|table|blockquote)/.test(p)) return p;
        return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');

    return s;
}

// ── Loading ───────────────────────────────────────────────────────────────────
function showLoading() {
    const id  = 'load-' + Date.now();
    const row = document.createElement('div');
    row.id        = id;
    row.className = 'msg-row assistant loading';

    const avatar = document.createElement('div');
    avatar.className  = 'msg-avatar';
    avatar.textContent = '⬡';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';

    row.append(avatar, bubble);
    messagesEl.appendChild(row);
    scrollBottom();
    return id;
}

// ── Utilitários ───────────────────────────────────────────────────────────────
function removeEl(id) {
    document.getElementById(id)?.remove();
}

function scrollBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function generateId() {
    return 'sess_' + Math.random().toString(36).slice(2, 11);
}

// ── Helpers públicos (chamados pelo HTML) ─────────────────────────────────────
function insertPrompt(text) {
    document.querySelector('.welcome')?.remove();
    msgInput.value = text;
    msgInput.dispatchEvent(new Event('input'));
    msgInput.focus();
    // Fecha sidebar no mobile
    document.querySelector('.sidebar')?.classList.remove('open');
}

function newSession() {
    sessionId = generateId();
    localStorage.setItem(SESSION_KEY, sessionId);
    messagesEl.innerHTML = `
        <div class="welcome">
            <div class="welcome-icon">⬡</div>
            <h2>Pronto para ajudar</h2>
            <p>Faça perguntas sobre processadores, memória, pipelining, sistemas de numeração ou peça para gerar PDFs e exercícios.</p>
        </div>`;
    msgInput.focus();
}

function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('open');
}