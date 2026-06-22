// === AGENTE IA RR98 - Frontend Dashboard ===
const API_URL = window.location.origin;

// === Navegação ===
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.dataset.page;
        document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
        link.classList.add('active');
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(`page-${page}`).classList.add('active');
        document.getElementById('pageTitle').textContent = link.textContent.trim();
        
        if (page === 'projects') loadProjects();
        if (page === 'whatsapp') loadChats();
        if (page === 'finance') loadFinance();
        if (page === 'monitor') loadMonitor();
    });
});

// === Dashboard - Atualização em tempo real ===
async function updateDashboard() {
    try {
        const [health, stats, finance] = await Promise.all([
            fetch(`${API_URL}/api/monitor/health`).then(r => r.json()),
            fetch(`${API_URL}/api/monitor/stats`).then(r => r.json()),
            fetch(`${API_URL}/api/payment/report`).then(r => r.json())
        ]);

        document.getElementById('statMessages').textContent = 
            (stats.messages?.sent || 0) + (stats.messages?.received || 0);
        document.getElementById('statRevenue').textContent = 
            `R$ ${(finance.totalRevenue || 0).toFixed(2)}`;
        document.getElementById('statBugFixes').textContent = stats.bugsFixed || 0;
        document.getElementById('statHealth').textContent = 
            health.status === 'healthy' ? '100%' : 'OK';
        document.getElementById('uptime').innerHTML = 
            `<i class="fas fa-clock"></i> ${Math.floor((stats.uptime || 0) / 3600)}h online`;

        addLog(`📊 Dashboard atualizado - Sistema ${health.status}`);
    } catch (error) {
        addLog(`❌ Erro ao atualizar dashboard: ${error.message}`);
    }
}

function addLog(message) {
    const log = document.getElementById('activityLog');
    const entry = document.createElement('p');
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    log.insertBefore(entry, log.firstChild);
    if (log.children.length > 50) log.removeChild(log.lastChild);
}

// === Chat IA ===
async function sendChat() {
    const prompt = document.getElementById('chatPrompt').value;
    const project = document.getElementById('chatProject').value;
    if (!prompt.trim()) return;

    const messages = document.getElementById('chatMessages');
    messages.innerHTML += `<div class="message user"><strong>Você:</strong> ${prompt}</div>`;
    document.getElementById('chatPrompt').value = '';

    try {
        const response = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, project })
        });
        const data = await response.json();
        
        messages.innerHTML += `<div class="message ai"><strong>🤖 RR98:</strong> ${data.reply || data.error}</div>`;
        messages.scrollTop = messages.scrollHeight;
    } catch (error) {
        messages.innerHTML += `<div class="message system">Erro: ${error.message}</div>`;
    }
}

// Enter to send
document.getElementById('chatPrompt')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
});

// === WhatsApp ===
async function loadChats() {
    try {
        const response = await fetch(`${API_URL}/api/whatsapp/chats`);
        const chats = await response.json();
        const list = document.getElementById('contactsList');
        list.innerHTML = chats.map(chat => `
            <div class="contact-item" onclick="viewChat('${chat.contact}')">
                <strong>${chat.contact}</strong>
                <small>${chat.project || 'geral'}</small>
                <p>${(chat.lastMessage?.message || '').substring(0, 50)}</p>
            </div>
        `).join('') || '<p class="log-empty">Nenhuma conversa ativa</p>';
    } catch {}
}

async function sendWhatsApp() {
    const to = document.getElementById('whatsContactInput').value;
    const message = document.getElementById('whatsMessageInput').value;
    if (!to || !message) return alert('Preencha contato e mensagem');

    try {
        const response = await fetch(`${API_URL}/api/whatsapp/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ to, message })
        });
        const data = await response.json();
        document.getElementById('whatsMessageInput').value = '';
        addLog(`📤 WhatsApp: Mensagem enviada para ${to}`);
        loadChats();
    } catch (error) {
        addLog(`❌ Erro WhatsApp: ${error.message}`);
    }
}

function viewChat(contact) {
    document.getElementById('whatsContactInput').value = contact;
    loadChatHistory(contact);
}

async function loadChatHistory(contact) {
    try {
        const response = await fetch(`${API_URL}/api/whatsapp/report`);
        const report = await response.json();
        const msgs = document.getElementById('whatsMessages');
        const chatMsgs = report.recentMessages?.filter(m => m.from === contact || m.to === contact) || [];
        
        msgs.innerHTML = chatMsgs.map(m => `
            <div class="${m.from === 'Agente RR98 🤖' ? 'msg-sent' : 'msg-received'}">
                <strong>${m.from}:</strong> ${m.message}
                <div class="msg-time">${new Date(m.timestamp).toLocaleString()}</div>
            </div>
        `).join('') || '<p class="chat-placeholder">Nenhuma mensagem neste chat</p>';
    } catch {}
}

// === Projetos ===
async function loadProjects() {
    try {
        const response = await fetch(`${API_URL}/api/projects/status`);
        const projects = await response.json();
        const grid = document.getElementById('projectsGrid');
        grid.innerHTML = projects.map(p => `
            <div class="project-card">
                <h3>${p.name}</h3>
                <span class="status-tag" style="background:${p.exists ? 'rgba(0,184,148,0.2);color:#00b894' : 'rgba(225,112,85,0.2);color:#e17055'}">
                    ${p.exists ? '✅ Ativo' : '❌ Ausente'}
                </span>
                <p>Tipo: ${p.type || 'desconhecido'}</p>
                <p>Arquivos: ${p.files || 0}</p>
                <p>Dependências: ${p.deps || 0}</p>
                ${p.scripts ? `<p>Scripts: ${p.scripts.join(', ')}</p>` : ''}
                <button class="action-btn" onclick="installProject('${p.name}')" style="margin-top:10px">
                    <i class="fas fa-download"></i> Instalar
                </button>
            </div>
        `).join('');
    } catch (error) {
        document.getElementById('projectsGrid').innerHTML = `<p>Erro ao carregar projetos: ${error.message}</p>`;
    }
}

async function installProject(name) {
    try {
        await fetch(`${API_URL}/api/project/install`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project: name })
        });
        addLog(`📦 Instalando dependências de ${name}...`);
        setTimeout(loadProjects, 3000);
    } catch (error) {
        addLog(`❌ Erro instalação ${name}: ${error.message}`);
    }
}

// === Financeiro ===
async function loadFinance() {
    try {
        const response = await fetch(`${API_URL}/api/payment/report`);
        const finance = await response.json();
        document.getElementById('financeStats').innerHTML = `
            <div class="stat-card"><h3>R$ ${(finance.totalRevenue || 0).toFixed(2)}</h3><p>Receita Total</p></div>
            <div class="stat-card"><h3>R$ ${(finance.improvementBudget || 0).toFixed(2)}</h3><p>Orçamento Melhorias</p></div>
            <div class="stat-card"><h3>${finance.pixKey}</h3><p>Chave PIX</p></div>
        `;
    } catch {}
}

// === Monitor ===
async function loadMonitor() {
    try {
        const [stats, health] = await Promise.all([
            fetch(`${API_URL}/api/monitor/stats`).then(r => r.json()),
            fetch(`${API_URL}/api/monitor/health`).then(r => r.json())
        ]);
        document.getElementById('monitorStats').innerHTML = `
            <div class="stat-card"><h3>${stats.requests?.total || 0}</h3><p>Requisições</p></div>
            <div class="stat-card"><h3>${stats.sales?.total || 0}</h3><p>Vendas</p></div>
            <div class="stat-card"><h3>${stats.bugsFixed || 0}</h3><p>Bugs Fixados</p></div>
            <div class="stat-card"><h3>${stats.optimizations || 0}</h3><p>Otimizações</p></div>
            <div class="stat-card"><h3>${Math.floor((stats.uptime || 0) / 3600)}h</h3><p>Uptime</p></div>
            <div class="stat-card"><h3>${health.status}</h3><p>Saúde</p></div>
        `;
    } catch {}
}

// === Ações Rápidas ===
async function sendMessage() {
    const msg = prompt('Mensagem para enviar via WhatsApp:');
    if (msg) {
        document.getElementById('whatsMessageInput').value = msg;
        document.querySelector('[data-page="whatsapp"]').click();
    }
}

async function scanSystem() {
    try {
        addLog('🔍 Escaneando sistema em busca de bugs...');
        const response = await fetch(`${API_URL}/api/system/scan-fix`, { method: 'POST' });
        const result = await response.json();
        addLog(`✅ Escaneamento concluído: ${result.length || 0} bugs encontrados`);
        updateDashboard();
    } catch (error) {
        addLog(`❌ Erro no escaneamento: ${error.message}`);
    }
}

async function diagnoseSystem() {
    try {
        addLog('🔍 Realizando diagnóstico completo...');
        const response = await fetch(`${API_URL}/api/system/diagnose`, { method: 'POST' });
        const result = await response.json();
        addLog(`✅ Diagnóstico: ${result.health} - ${result.issues?.length || 0} issue(s)`);
        updateDashboard();
    } catch (error) {
        addLog(`❌ Erro no diagnóstico: ${error.message}`);
    }
}

async function optimizeSystem() {
    try {
        addLog('⚡ Otimizando sistema...');
        const response = await fetch(`${API_URL}/api/system/optimize`, { method: 'POST' });
        const result = await response.json();
        addLog(`✅ ${result.optimizations?.length || 0} otimizações aplicadas`);
        updateDashboard();
    } catch (error) {
        addLog(`❌ Erro na otimização: ${error.message}`);
    }
}

// === Configurações ===
async function saveSettings() {
    const groqKey = document.getElementById('groqKey').value;
    if (groqKey) {
        localStorage.setItem('GROQ_API_KEY', groqKey);
        addLog('🔑 Chave API Groq salva');
    }
    addLog('⚙️ Configurações salvas com sucesso!');
}

// === Inicialização ===
setInterval(updateDashboard, 10000);
updateDashboard();
loadChats();
addLog('🚀 Agente IA RR98 inicializado e pronto para operar!');
addLog('💰 Chave PIX: 046999732012');
addLog('📱 WhatsApp Virtual ativo');