/**
 * DevAgent Hub - Main Application Logic
 * Gerencia navegação, modais, CRUD e renderização
 */

// ─── Navigation ───

document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();
        const page = this.dataset.page;
        navigateTo(page);
    });
});

function navigateTo(page) {
    // Update nav items
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector(`.nav-item[data-page="${page}"]`)?.classList.add('active');
    
    // Update pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const targetPage = document.getElementById(`page-${page}`);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Load data for page
    switch(page) {
        case 'dashboard': loadDashboard(); break;
        case 'projects': loadProjects(); break;
        case 'tasks': loadTasks(); break;
        case 'prompts': loadPrompts(); break;
        case 'docs': loadDocs(); break;
    }
}

// ─── Menu Toggle ───

document.getElementById('menuToggle')?.addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

// Close sidebar on outside click (mobile)
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('menuToggle');
    if (window.innerWidth <= 768 && 
        sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) && 
        !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});

// ─── Theme ───

function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme === 'light' ? 'light' : '');
    localStorage.setItem('devagent_theme', theme);
}

// Load saved theme
const savedTheme = localStorage.getItem('devagent_theme') || 'dark';
document.getElementById('themeSelect').value = savedTheme;
changeTheme(savedTheme);

// ─── Global Search ───

document.getElementById('globalSearch')?.addEventListener('input', function() {
    const query = this.value.toLowerCase().trim();
    // Search across all visible items
    document.querySelectorAll('.prompt-card, .doc-card, .task-card, tr[data-search]').forEach(el => {
        const text = el.textContent.toLowerCase();
        el.style.display = text.includes(query) ? '' : 'none';
    });
});

// ─── Toast System ───

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: 'check-circle',
        error: 'times-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    
    toast.innerHTML = `<i class="fas fa-${icons[type] || icons.info}"></i> ${message}`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ─── Modal System ───

function openModal(title, content) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').innerHTML = content;
    document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modalOverlay').classList.remove('active');
}

// Close modal on overlay click
document.getElementById('modalOverlay')?.addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

// Close on Escape
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
});

// ─── Refresh Button ───

document.getElementById('refreshBtn')?.addEventListener('click', () => {
    const activePage = document.querySelector('.page.active');
    if (activePage) {
        const pageId = activePage.id.replace('page-', '');
        navigateTo(pageId);
        showToast('Dados atualizados', 'success');
    }
});

// ─── Dashboard ───

async function loadDashboard() {
    const projects = await api.getProjects();
    const tasks = await api.getTasks();
    const prompts = await api.getPrompts();
    const docs = await api.getDocs();

    // Stats
    document.getElementById('statProjects').textContent = projects.filter(p => p.status === 'ativo' || !p.status).length;
    document.getElementById('statTasks').textContent = tasks.filter(t => t.status === 'todo' || t.status === 'doing').length;
    document.getElementById('statPrompts').textContent = prompts.length;
    document.getElementById('statDocs').textContent = docs.length;

    // Recent Activity
    const activities = api.getActivities();
    const activityContainer = document.getElementById('recentActivity');
    
    if (activities.length === 0) {
        activityContainer.innerHTML = '<p class="empty-state">Nenhuma atividade recente</p>';
    } else {
        activityContainer.innerHTML = activities.slice(0, 10).map(a => {
            const icons = { create: 'plus-circle', update: 'edit', delete: 'trash' };
            const colors = { create: '#00e676', update: '#448aff', delete: '#ff1744' };
            const typeNames = { project: 'Projeto', task: 'Tarefa', prompt: 'Prompt', doc: 'Documento' };
            const actionNames = { create: 'Criou', update: 'Editou', delete: 'Removeu' };
            
            return `
                <div class="activity-item">
                    <i class="fas fa-${icons[a.action] || 'circle'}" style="color: ${colors[a.action] || '#888'}"></i>
                    <span><strong>${actionNames[a.action] || a.action}</strong> ${typeNames[a.type] || a.type}: ${a.name}</span>
                    <small>${formatDate(a.timestamp)}</small>
                </div>
            `;
        }).join('');
    }
}

// ─── Projects ───

async function loadProjects() {
    const projects = await api.getProjects();
    const searchTerm = document.getElementById('projectSearch')?.value?.toLowerCase() || '';
    const statusFilter = document.getElementById('projectStatusFilter')?.value || 'all';
    
    const filtered = projects.filter(p => {
        const matchesSearch = p.nome?.toLowerCase().includes(searchTerm) || 
                             p.descricao?.toLowerCase().includes(searchTerm);
        const matchesStatus = statusFilter === 'all' || p.status === statusFilter;
        return matchesSearch && matchesStatus;
    });

    const tbody = document.getElementById('projectsBody');
    
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Nenhum projeto encontrado</td></tr>';
        return;
    }

    tbody.innerHTML = filtered.map(p => `
        <tr data-search="${p.nome} ${p.descricao}">
            <td><strong>${p.nome}</strong></td>
            <td>${p.descricao?.substring(0, 50) || '-'}${p.descricao?.length > 50 ? '...' : ''}</td>
            <td><span class="status-badge ${p.status || 'ativo'}">${p.status || 'ativo'}</span></td>
            <td>
                <div class="tech-tags">
                    ${(p.tecnologias || '').split(',').filter(t => t.trim()).map(t => 
                        `<span class="tech-tag">${t.trim()}</span>`
                    ).join('')}
                </div>
            </td>
            <td>${formatDate(p.created_at)}</td>
            <td>
                <div class="btn-group">
                    <button class="btn btn-sm btn-info" onclick="editProject('${p.id}')" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteProject('${p.id}')" title="Excluir">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Project filters
document.getElementById('projectSearch')?.addEventListener('input', loadProjects);
document.getElementById('projectStatusFilter')?.addEventListener('change', loadProjects);

function openProjectModal(project = null) {
    const isEdit = !!project;
    const content = `
        <form id="projectForm" onsubmit="saveProject(event)">
            <input type="hidden" id="projectId" value="${project?.id || ''}">
            <div class="form-group">
                <label>Nome do Projeto *</label>
                <input type="text" id="projectNome" class="form-input" value="${project?.nome || ''}" required 
                       placeholder="Ex: Meu SaaS Financeiro">
            </div>
            <div class="form-group">
                <label>Descrição</label>
                <textarea id="projectDescricao" class="form-textarea" placeholder="Descreva o objetivo do projeto...">${project?.descricao || ''}</textarea>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select id="projectStatus" class="form-select">
                    <option value="ativo" ${project?.status === 'ativo' ? 'selected' : ''}>Ativo</option>
                    <option value="pausado" ${project?.status === 'pausado' ? 'selected' : ''}>Pausado</option>
                    <option value="concluido" ${project?.status === 'concluido' ? 'selected' : ''}>Concluído</option>
                    <option value="arquivado" ${project?.status === 'arquivado' ? 'selected' : ''}>Arquivado</option>
                </select>
            </div>
            <div class="form-group">
                <label>Tecnologias (separadas por vírgula)</label>
                <input type="text" id="projectTecnologias" class="form-input" value="${project?.tecnologias || ''}" 
                       placeholder="Ex: React, Node.js, Supabase">
            </div>
            <div class="form-group">
                <label>Link do Repositório</label>
                <input type="url" id="projectLink" class="form-input" value="${project?.link || ''}" 
                       placeholder="https://github.com/usuario/projeto">
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center">
                <i class="fas fa-save"></i> ${isEdit ? 'Atualizar' : 'Criar'} Projeto
            </button>
        </form>
    `;
    openModal(isEdit ? 'Editar Projeto' : 'Novo Projeto', content);
}

async function saveProject(e) {
    e.preventDefault();
    const id = document.getElementById('projectId').value;
    const data = {
        nome: document.getElementById('projectNome').value,
        descricao: document.getElementById('projectDescricao').value,
        status: document.getElementById('projectStatus').value,
        tecnologias: document.getElementById('projectTecnologias').value,
        link: document.getElementById('projectLink').value
    };

    try {
        if (id) {
            await api.updateProject(id, data);
            showToast('Projeto atualizado com sucesso!', 'success');
        } else {
            await api.createProject(data);
            showToast('Projeto criado com sucesso!', 'success');
        }
        closeModal();
        loadProjects();
        loadDashboard();
    } catch (e) {
        showToast('Erro ao salvar projeto: ' + e.message, 'error');
    }
}

async function editProject(id) {
    const projects = await api.getProjects();
    const project = projects.find(p => p.id === id);
    if (project) openProjectModal(project);
}

async function deleteProject(id) {
    if (!confirm('Tem certeza que deseja excluir este projeto?')) return;
    try {
        await api.deleteProject(id);
        showToast('Projeto excluído', 'success');
        loadProjects();
        loadDashboard();
    } catch (e) {
        showToast('Erro ao excluir: ' + e.message, 'error');
    }
}

// ─── Tasks (Kanban) ───

async function loadTasks() {
    const tasks = await api.getTasks();
    
    const columns = {
        todo: document.getElementById('todoList'),
        doing: document.getElementById('doingList'),
        done: document.getElementById('doneList')
    };

    ['todo', 'doing', 'done'].forEach(status => {
        const filtered = tasks.filter(t => t.status === status);
        const container = columns[status];
        const countEl = document.getElementById(`${status}Count`);
        
        if (countEl) countEl.textContent = filtered.length;

        if (filtered.length === 0) {
            container.innerHTML = '<p class="empty-state">Nenhuma tarefa</p>';
        } else {
            container.innerHTML = filtered.map(t => `
                <div class="task-card" draggable="true" data-id="${t.id}" ondragstart="dragTask(event)" 
                     onclick="openTaskView('${t.id}')">
                    <div class="task-title">${t.titulo}</div>
                    ${t.descricao ? `<div class="task-description">${t.descricao.substring(0, 60)}${t.descricao.length > 60 ? '...' : ''}</div>` : ''}
                    <div class="task-meta">
                        <span class="task-priority ${t.prioridade || 'media'}">${t.prioridade || 'média'}</span>
                        <span class="task-date">${formatDate(t.created_at)}</span>
                    </div>
                </div>
            `).join('');
        }
    });
}

// Drag and drop for Kanban
function dragTask(e) {
    e.dataTransfer.setData('text/plain', e.target.closest('.task-card').dataset.id);
}

document.querySelectorAll('.kanban-body').forEach(column => {
    column.addEventListener('dragover', e => {
        e.preventDefault();
        column.style.background = 'rgba(0, 212, 255, 0.05)';
    });

    column.addEventListener('dragleave', () => {
        column.style.background = '';
    });

    column.addEventListener('drop', async function(e) {
        e.preventDefault();
        this.style.background = '';
        const taskId = e.dataTransfer.getData('text/plain');
        const newStatus = this.closest('.kanban-column').dataset.status;
        
        if (taskId && newStatus) {
            await api.updateTask(taskId, { status: newStatus });
            loadTasks();
            loadDashboard();
            showToast('Tarefa movida com sucesso!', 'success');
        }
    });
});

function openTaskModal(task = null) {
    const isEdit = !!task;
    const content = `
        <form id="taskForm" onsubmit="saveTask(event)">
            <input type="hidden" id="taskId" value="${task?.id || ''}">
            <div class="form-group">
                <label>Título da Tarefa *</label>
                <input type="text" id="taskTitulo" class="form-input" value="${task?.titulo || ''}" required
                       placeholder="Ex: Criar tela de login">
            </div>
            <div class="form-group">
                <label>Descrição</label>
                <textarea id="taskDescricao" class="form-textarea" placeholder="Descreva a tarefa...">${task?.descricao || ''}</textarea>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select id="taskStatus" class="form-select">
                    <option value="todo" ${task?.status === 'todo' || !task ? 'selected' : ''}>A Fazer</option>
                    <option value="doing" ${task?.status === 'doing' ? 'selected' : ''}>Fazendo</option>
                    <option value="done" ${task?.status === 'done' ? 'selected' : ''}>Concluído</option>
                </select>
            </div>
            <div class="form-group">
                <label>Prioridade</label>
                <select id="taskPrioridade" class="form-select">
                    <option value="baixa" ${task?.prioridade === 'baixa' ? 'selected' : ''}>Baixa</option>
                    <option value="media" ${task?.prioridade === 'media' || !task ? 'selected' : ''}>Média</option>
                    <option value="alta" ${task?.prioridade === 'alta' ? 'selected' : ''}>Alta</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center">
                <i class="fas fa-save"></i> ${isEdit ? 'Atualizar' : 'Criar'} Tarefa
            </button>
        </form>
    `;
    openModal(isEdit ? 'Editar Tarefa' : 'Nova Tarefa', content);
}

async function saveTask(e) {
    e.preventDefault();
    const id = document.getElementById('taskId').value;
    const data = {
        titulo: document.getElementById('taskTitulo').value,
        descricao: document.getElementById('taskDescricao').value,
        status: document.getElementById('taskStatus').value,
        prioridade: document.getElementById('taskPrioridade').value
    };

    try {
        if (id) {
            await api.updateTask(id, data);
            showToast('Tarefa atualizada!', 'success');
        } else {
            await api.createTask(data);
            showToast('Tarefa criada!', 'success');
        }
        closeModal();
        loadTasks();
        loadDashboard();
    } catch (e) {
        showToast('Erro ao salvar tarefa: ' + e.message, 'error');
    }
}

async function openTaskView(id) {
    const tasks = await api.getTasks();
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    const content = `
        <div style="margin-bottom:20px">
            <h3 style="font-size:1.2rem;margin-bottom:8px">${task.titulo}</h3>
            <p style="color:var(--text-secondary);margin-bottom:16px">${task.descricao || 'Sem descrição'}</p>
            <div style="display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap">
                <span class="status-badge ${task.status || 'todo'}">${getStatusName(task.status)}</span>
                <span class="task-priority ${task.prioridade || 'media'}">${task.prioridade || 'média'}</span>
                <small style="color:var(--text-secondary)">Criado: ${formatDate(task.created_at)}</small>
            </div>
        </div>
        <div style="display:flex;gap:8px">
            <button class="btn btn-info" onclick="editTaskFromView('${task.id}')">
                <i class="fas fa-edit"></i> Editar
            </button>
            <button class="btn btn-danger" onclick="deleteTask('${task.id}')">
                <i class="fas fa-trash"></i> Excluir
            </button>
        </div>
    `;
    openModal('Detalhes da Tarefa', content);
}

function getStatusName(status) {
    const names = { todo: 'A Fazer', doing: 'Fazendo', done: 'Concluído' };
    return names[status] || status;
}

async function editTaskFromView(id) {
    const tasks = await api.getTasks();
    const task = tasks.find(t => t.id === id);
    if (task) {
        closeModal();
        openTaskModal(task);
    }
}

async function deleteTask(id) {
    if (!confirm('Excluir esta tarefa?')) return;
    try {
        await api.deleteTask(id);
        closeModal();
        loadTasks();
        loadDashboard();
        showToast('Tarefa excluída', 'success');
    } catch (e) {
        showToast('Erro ao excluir: ' + e.message, 'error');
    }
}

// ─── Prompts ───

async function loadPrompts() {
    const prompts = await api.getPrompts();
    const searchTerm = document.getElementById('promptSearch')?.value?.toLowerCase() || '';
    const categoryFilter = document.getElementById('promptCategoryFilter')?.value || 'all';
    
    const filtered = prompts.filter(p => {
        const matchesSearch = p.titulo?.toLowerCase().includes(searchTerm) || 
                             p.conteudo?.toLowerCase().includes(searchTerm);
        const matchesCategory = categoryFilter === 'all' || p.categoria === categoryFilter;
        return matchesSearch && matchesCategory;
    });

    const grid = document.getElementById('promptsGrid');
    
    if (filtered.length === 0) {
        grid.innerHTML = '<p class="empty-state">Nenhum prompt encontrado</p>';
        return;
    }

    grid.innerHTML = filtered.map(p => `
        <div class="prompt-card" onclick="viewPrompt('${p.id}')">
            <div class="prompt-title">${p.titulo}</div>
            <div class="prompt-content">${p.conteudo}</div>
            <div class="prompt-meta">
                <span class="prompt-category">${getCategoryName(p.categoria)}</span>
                <small style="color:var(--text-secondary)">${formatDate(p.created_at)}</small>
            </div>
        </div>
    `).join('');
}

function getCategoryName(cat) {
    const names = {
        'desenvolvimento': 'Desenvolvimento',
        'arquitetura': 'Arquitetura',
        'banco-dados': 'Banco de Dados',
        'frontend': 'Frontend',
        'backend': 'Backend',
        'deploy': 'Deploy'
    };
    return names[cat] || cat || 'Geral';
}

document.getElementById('promptSearch')?.addEventListener('input', loadPrompts);
document.getElementById('promptCategoryFilter')?.addEventListener('change', loadPrompts);

function openPromptModal(prompt = null) {
    const isEdit = !!prompt;
    const content = `
        <form id="promptForm" onsubmit="savePrompt(event)">
            <input type="hidden" id="promptId" value="${prompt?.id || ''}">
            <div class="form-group">
                <label>Título do Prompt *</label>
                <input type="text" id="promptTitulo" class="form-input" value="${prompt?.titulo || ''}" required
                       placeholder="Ex: Gerar API REST">
            </div>
            <div class="form-group">
                <label>Conteúdo do Prompt *</label>
                <textarea id="promptConteudo" class="form-textarea" style="min-height:150px" required
                          placeholder="Cole o prompt completo aqui...">${prompt?.conteudo || ''}</textarea>
            </div>
            <div class="form-group">
                <label>Categoria</label>
                <select id="promptCategoria" class="form-select">
                    <option value="desenvolvimento" ${prompt?.categoria === 'desenvolvimento' ? 'selected' : ''}>Desenvolvimento</option>
                    <option value="arquitetura" ${prompt?.categoria === 'arquitetura' ? 'selected' : ''}>Arquitetura</option>
                    <option value="banco-dados" ${prompt?.categoria === 'banco-dados' ? 'selected' : ''}>Banco de Dados</option>
                    <option value="frontend" ${prompt?.categoria === 'frontend' ? 'selected' : ''}>Frontend</option>
                    <option value="backend" ${prompt?.categoria === 'backend' ? 'selected' : ''}>Backend</option>
                    <option value="deploy" ${prompt?.categoria === 'deploy' ? 'selected' : ''}>Deploy</option>
                </select>
            </div>
            <div style="display:flex;gap:8px">
                <button type="submit" class="btn btn-primary" style="flex:1;justify-content:center">
                    <i class="fas fa-save"></i> ${isEdit ? 'Atualizar' : 'Salvar'}
                </button>
                <button type="button" class="btn btn-warning" onclick="copyPromptFromForm()" style="justify-content:center">
                    <i class="fas fa-copy"></i> Copiar
                </button>
            </div>
        </form>
    `;
    openModal(isEdit ? 'Editar Prompt' : 'Novo Prompt', content);
}

function copyPromptFromForm() {
    const content = document.getElementById('promptConteudo')?.value;
    if (content) {
        navigator.clipboard.writeText(content).then(() => {
            showToast('Prompt copiado para área de transferência!', 'success');
        }).catch(() => {
            showToast('Erro ao copiar', 'error');
        });
    }
}

async function savePrompt(e) {
    e.preventDefault();
    const id = document.getElementById('promptId').value;
    const data = {
        titulo: document.getElementById('promptTitulo').value,
        conteudo: document.getElementById('promptConteudo').value,
        categoria: document.getElementById('promptCategoria').value
    };

    try {
        if (id) {
            await api.updatePrompt(id, data);
            showToast('Prompt atualizado!', 'success');
        } else {
            await api.createPrompt(data);
            showToast('Prompt salvo!', 'success');
        }
        closeModal();
        loadPrompts();
        loadDashboard();
    } catch (e) {
        showToast('Erro ao salvar prompt: ' + e.message, 'error');
    }
}

async function viewPrompt(id) {
    const prompts = await api.getPrompts();
    const prompt = prompts.find(p => p.id === id);
    if (!prompt) return;

    const content = `
        <div style="margin-bottom:16px">
            <h3 style="font-size:1.1rem;margin-bottom:8px">${prompt.titulo}</h3>
            <span class="prompt-category">${getCategoryName(prompt.categoria)}</span>
        </div>
        <div style="background:var(--main-bg);padding:16px;border-radius:8px;margin-bottom:16px;max-height:300px;overflow-y:auto;white-space:pre-wrap;font-size:0.85rem">
            ${prompt.conteudo}
        </div>
        <div style="display:flex;gap:8px">
            <button class="btn btn-warning" onclick="copyPrompt('${id}')">
                <i class="fas fa-copy"></i> Copiar
            </button>
            <button class="btn btn-info" onclick="editPrompt('${id}')">
                <i class="fas fa-edit"></i> Editar
            </button>
            <button class="btn btn-danger" onclick="deletePrompt('${id}')">
                <i class="fas fa-trash"></i> Excluir
            </button>
        </div>
    `;
    openModal('Visualizar Prompt', content);
}

async function copyPrompt(id) {
    const prompts = await api.getPrompts();
    const prompt = prompts.find(p => p.id === id);
    if (prompt?.conteudo) {
        navigator.clipboard.writeText(prompt.conteudo).then(() => {
            showToast('Prompt copiado!', 'success');
        });
    }
}

async function editPrompt(id) {
    const prompts = await api.getPrompts();
    const prompt = prompts.find(p => p.id === id);
    if (prompt) {
        closeModal();
        openPromptModal(prompt);
    }
}

async function deletePrompt(id) {
    if (!confirm('Excluir este prompt?')) return;
    try {
        await api.deletePrompt(id);
        closeModal();
        loadPrompts();
        loadDashboard();
        showToast('Prompt excluído', 'success');
    } catch (e) {
        showToast('Erro ao excluir: ' + e.message, 'error');
    }
}

// ─── Documents ───

async function loadDocs() {
    const docs = await api.getDocs();
    const searchTerm = document.getElementById('docSearch')?.value?.toLowerCase() || '';
    const typeFilter = document.getElementById('docTypeFilter')?.value || 'all';
    
    const filtered = docs.filter(d => {
        const matchesSearch = d.titulo?.toLowerCase().includes(searchTerm) || 
                             d.conteudo?.toLowerCase().includes(searchTerm);
        const matchesType = typeFilter === 'all' || d.tipo === typeFilter;
        return matchesSearch && matchesType;
    });

    const grid = document.getElementById('docsGrid');
    
    if (filtered.length === 0) {
        grid.innerHTML = '<p class="empty-state">Nenhum documento encontrado</p>';
        return;
    }

    const typeIcons = { nota: 'sticky-note', tutorial: 'graduation-cap', ideia: 'lightbulb', documentacao: 'file-alt' };
    const typeColors = { nota: '#8888aa', tutorial: '#00d4ff', ideia: '#ffab00', documentacao: '#00e676' };

    grid.innerHTML = filtered.map(d => `
        <div class="doc-card" onclick="viewDoc('${d.id}')">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                <i class="fas fa-${typeIcons[d.tipo] || 'file'}" style="color:${typeColors[d.tipo] || '#888'}"></i>
                <div class="doc-title">${d.titulo}</div>
            </div>
            <div class="doc-content">${d.conteudo}</div>
            <div class="doc-meta">
                <small style="color:var(--text-secondary)">${getTypeName(d.tipo)}</small>
                <small style="color:var(--text-secondary)">${formatDate(d.created_at)}</small>
            </div>
        </div>
    `).join('');
}

function getTypeName(type) {
    const names = { nota: 'Nota', tutorial: 'Tutorial', ideia: 'Ideia', documentacao: 'Documentação' };
    return names[type] || type || 'Geral';
}

document.getElementById('docSearch')?.addEventListener('input', loadDocs);
document.getElementById('docTypeFilter')?.addEventListener('change', loadDocs);

function openDocModal(doc = null) {
    const isEdit = !!doc;
    const content = `
        <form id="docForm" onsubmit="saveDoc(event)">
            <input type="hidden" id="docId" value="${doc?.id || ''}">
            <div class="form-group">
                <label>Título *</label>
                <input type="text" id="docTitulo" class="form-input" value="${doc?.titulo || ''}" required
                       placeholder="Ex: Como fazer deploy no Cloudflare">
            </div>
            <div class="form-group">
                <label>Conteúdo *</label>
                <textarea id="docConteudo" class="form-textarea" style="min-height:200px" required
                          placeholder="Escreva sua documentação aqui...">${doc?.conteudo || ''}</textarea>
            </div>
            <div class="form-group">
                <label>Tipo</label>
                <select id="docTipo" class="form-select">
                    <option value="nota" ${doc?.tipo === 'nota' ? 'selected' : ''}>Nota</option>
                    <option value="tutorial" ${doc?.tipo === 'tutorial' ? 'selected' : ''}>Tutorial</option>
                    <option value="ideia" ${doc?.tipo === 'ideia' ? 'selected' : ''}>Ideia</option>
                    <option value="documentacao" ${doc?.tipo === 'documentacao' ? 'selected' : ''}>Documentação</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center">
                <i class="fas fa-save"></i> ${isEdit ? 'Atualizar' : 'Salvar'}
            </button>
        </form>
    `;
    openModal(isEdit ? 'Editar Documento' : 'Nova Documentação', content);
}

async function saveDoc(e) {
    e.preventDefault();
    const id = document.getElementById('docId').value;
    const data = {
        titulo: document.getElementById('docTitulo').value,
        conteudo: document.getElementById('docConteudo').value,
        tipo: document.getElementById('docTipo').value
    };

    try {
        if (id) {
            await api.updateDoc(id, data);
            showToast('Documento atualizado!', 'success');
        } else {
            await api.createDoc(data);
            showToast('Documento criado!', 'success');
        }
        closeModal();
        loadDocs();
        loadDashboard();
    } catch (e) {
        showToast('Erro ao salvar: ' + e.message, 'error');
    }
}

async function viewDoc(id) {
    const docs = await api.getDocs();
    const doc = docs.find(d => d.id === id);
    if (!doc) return;

    const typeIcons = { nota: 'sticky-note', tutorial: 'graduation-cap', ideia: 'lightbulb', documentacao: 'file-alt' };
    const typeColors = { nota: '#8888aa', tutorial: '#00d4ff', ideia: '#ffab00', documentacao: '#00e676' };

    const content = `
        <div style="margin-bottom:16px;display:flex;align-items:center;gap:8px">
            <i class="fas fa-${typeIcons[doc.tipo] || 'file'}" style="color:${typeColors[doc.tipo] || '#888'};font-size:1.2rem"></i>
            <h3 style="font-size:1.1rem">${doc.titulo}</h3>
        </div>
        <div style="background:var(--main-bg);padding:16px;border-radius:8px;margin-bottom:16px;max-height:350px;overflow-y:auto;white-space:pre-wrap;font-size:0.9rem">
            ${doc.conteudo}
        </div>
        <div style="display:flex;gap:8px">
            <button class="btn btn-info" onclick="editDoc('${doc.id}')">
                <i class="fas fa-edit"></i> Editar
            </button>
            <button class="btn btn-danger" onclick="deleteDoc('${doc.id}')">
                <i class="fas fa-trash"></i> Excluir
            </button>
        </div>
    `;
    openModal('Visualizar Documento', content);
}

async function editDoc(id) {
    const docs = await api.getDocs();
    const doc = docs.find(d => d.id === id);
    if (doc) {
        closeModal();
        openDocModal(doc);
    }
}

async function deleteDoc(id) {
    if (!confirm('Excluir este documento?')) return;
    try {
        await api.deleteDoc(id);
        closeModal();
        loadDocs();
        loadDashboard();
        showToast('Documento excluído', 'success');
    } catch (e) {
        showToast('Erro ao excluir: ' + e.message, 'error');
    }
}

// ─── Master Prompt ───

function openMasterPrompt() {
    const masterPrompt = `Você é meu arquiteto de software e desenvolvedor full stack.

Quando eu pedir qualquer projeto:

1. Analise o objetivo.
2. Defina a arquitetura.
3. Crie a estrutura de pastas.
4. Gere todos os arquivos necessários.
5. Gere banco de dados.
6. Gere API.
7. Gere frontend.
8. Gere documentação.
9. Explique implantação.
10. Liste melhorias futuras.

Sempre entregue código completo e funcional.`;

    navigator.clipboard.writeText(masterPrompt).then(() => {
        showToast('Prompt Mestre copiado para área de transferência!', 'success');
    }).catch(() => {
        showToast('Erro ao copiar', 'error');
    });
}

// ─── Supabase Config ───

async function saveSupabaseConfig() {
    const url = document.getElementById('supabaseUrl').value.trim();
    const key = document.getElementById('supabaseKey').value.trim();

    if (!url || !key) {
        showToast('Preencha URL e Anon Key do Supabase', 'warning');
        return;
    }

    const btn = document.querySelector('#page-settings .btn-primary');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Conectando...';

    const success = await api.connectSupabase(url, key);

    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-save"></i> Salvar & Conectar';

    if (success) {
        showToast('Conectado ao Supabase com sucesso!', 'success');
        loadDashboard();
    } else {
        showToast('Modo Local ativado. Dados salvos no navegador.', 'info');
    }
}

// ─── Export / Import ───

function exportAllData() {
    const data = api.exportAllData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `devagent-hub-backup-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Dados exportados com sucesso!', 'success');
}

function importData(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (api.importAllData(data)) {
                showToast('Dados importados com sucesso!', 'success');
                // Recarregar página atual
                const activePage = document.querySelector('.page.active');
                if (activePage) {
                    const pageId = activePage.id.replace('page-', '');
                    navigateTo(pageId);
                }
                loadDashboard();
            }
        } catch (err) {
            showToast('Erro ao importar: arquivo inválido', 'error');
        }
    };
    reader.readAsText(file);
    event.target.value = '';
}

// ─── Utility Functions ───

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ─── Activity Styles (inject) ───

const activityStyles = document.createElement('style');
activityStyles.textContent = `
    .activity-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid var(--border);
        font-size: 0.85rem;
    }
    .activity-item:last-child { border-bottom: none; }
    .activity-item i { font-size: 0.9rem; width: 20px; }
    .activity-item small {
        margin-left: auto;
        color: var(--text-secondary);
        font-size: 0.75rem;
        white-space: nowrap;
    }
    .kanban-body.drag-over {
        background: rgba(0, 212, 255, 0.1) !important;
    }
`;
document.head.appendChild(activityStyles);

// ─── Initialize ───

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});