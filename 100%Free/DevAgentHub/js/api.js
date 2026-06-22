/**
 * DevAgent Hub - API Service
 * Integração com Supabase e armazenamento local (fallback)
 */

class DevAgentAPI {
    constructor() {
        this.supabaseUrl = '';
        this.supabaseKey = '';
        this.isConnected = false;
        this.useLocalStorage = true;
        this.db = null;
        this.init();
    }

    async init() {
        // Carregar configurações salvas
        const config = this.getLocalConfig();
        if (config.supabaseUrl && config.supabaseKey) {
            this.supabaseUrl = config.supabaseUrl;
            this.supabaseKey = config.supabaseKey;
            await this.connectSupabase();
        }
    }

    getLocalConfig() {
        try {
            const saved = localStorage.getItem('devagent_config');
            return saved ? JSON.parse(saved) : {};
        } catch {
            return {};
        }
    }

    saveLocalConfig(config) {
        const current = this.getLocalConfig();
        const updated = { ...current, ...config };
        localStorage.setItem('devagent_config', JSON.stringify(updated));
    }

    async connectSupabase(url, key) {
        if (url && key) {
            this.supabaseUrl = url;
            this.supabaseKey = key;
            this.saveLocalConfig({ supabaseUrl: url, supabaseKey: key });
        }

        if (!this.supabaseUrl || !this.supabaseKey) {
            this.isConnected = false;
            this.useLocalStorage = true;
            this.updateConnectionStatus(false);
            return false;
        }

        try {
            // Tentar conectar via fetch direto (sem SDK)
            const response = await fetch(`${this.supabaseUrl}/rest/v1/`, {
                headers: {
                    'apikey': this.supabaseKey,
                    'Authorization': `Bearer ${this.supabaseKey}`
                }
            });

            if (response.ok || response.status === 200) {
                this.isConnected = true;
                this.useLocalStorage = false;
                this.updateConnectionStatus(true);
                return true;
            }
        } catch (e) {
            console.warn('Supabase connection failed, using localStorage:', e.message);
        }

        this.isConnected = false;
        this.useLocalStorage = true;
        this.updateConnectionStatus(false);
        return false;
    }

    updateConnectionStatus(online) {
        const dot = document.querySelector('.status-dot');
        const text = document.getElementById('statusText');
        if (dot && text) {
            dot.className = `status-dot ${online ? 'online' : 'offline'}`;
            text.textContent = online ? 'Conectado ao Supabase' : 'Modo Local';
        }
    }

    // ─── Supabase REST helpers ───

    async supabaseFetch(table, options = {}) {
        const { method = 'GET', body, params = '' } = options;
        const url = `${this.supabaseUrl}/rest/v1/${table}${params}`;

        try {
            const response = await fetch(url, {
                method,
                headers: {
                    'apikey': this.supabaseKey,
                    'Authorization': `Bearer ${this.supabaseKey}`,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation'
                },
                body: body ? JSON.stringify(body) : undefined
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (e) {
            console.error(`Supabase ${method} ${table} failed:`, e.message);
            throw e;
        }
    }

    // ─── Local Storage CRUD ───

    getLocalData(key) {
        try {
            const data = localStorage.getItem(`devagent_${key}`);
            return data ? JSON.parse(data) : [];
        } catch {
            return [];
        }
    }

    setLocalData(key, data) {
        localStorage.setItem(`devagent_${key}`, JSON.stringify(data));
    }

    // ─── Projects ───

    async getProjects() {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('projects', {
                    params: '?order=created_at.desc'
                });
            } catch {
                // fallback para local
            }
        }
        return this.getLocalData('projects');
    }

    async createProject(project) {
        const newProject = {
            ...project,
            id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        };

        if (!this.useLocalStorage) {
            try {
                const result = await this.supabaseFetch('projects', {
                    method: 'POST',
                    body: newProject
                });
                return result[0] || newProject;
            } catch {
                // fallback
            }
        }

        const projects = this.getLocalData('projects');
        projects.push(newProject);
        this.setLocalData('projects', projects);
        this.logActivity('create', 'project', newProject.nome);
        return newProject;
    }

    async updateProject(id, updates) {
        updates.updated_at = new Date().toISOString();

        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('projects', {
                    method: 'PATCH',
                    body: updates,
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        const projects = this.getLocalData('projects');
        const index = projects.findIndex(p => p.id === id);
        if (index !== -1) {
            projects[index] = { ...projects[index], ...updates };
            this.setLocalData('projects', projects);
        }
        return projects[index];
    }

    async deleteProject(id) {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('projects', {
                    method: 'DELETE',
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        let projects = this.getLocalData('projects');
        projects = projects.filter(p => p.id !== id);
        this.setLocalData('projects', projects);
        return true;
    }

    // ─── Tasks ───

    async getTasks() {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('tasks', {
                    params: '?order=created_at.desc'
                });
            } catch {
                // fallback
            }
        }
        return this.getLocalData('tasks');
    }

    async createTask(task) {
        const newTask = {
            ...task,
            id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        };

        if (!this.useLocalStorage) {
            try {
                const result = await this.supabaseFetch('tasks', {
                    method: 'POST',
                    body: newTask
                });
                return result[0] || newTask;
            } catch {
                // fallback
            }
        }

        const tasks = this.getLocalData('tasks');
        tasks.push(newTask);
        this.setLocalData('tasks', tasks);
        this.logActivity('create', 'task', newTask.titulo);
        return newTask;
    }

    async updateTask(id, updates) {
        updates.updated_at = new Date().toISOString();

        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('tasks', {
                    method: 'PATCH',
                    body: updates,
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        const tasks = this.getLocalData('tasks');
        const index = tasks.findIndex(t => t.id === id);
        if (index !== -1) {
            tasks[index] = { ...tasks[index], ...updates };
            this.setLocalData('tasks', tasks);
        }
        return tasks[index];
    }

    async deleteTask(id) {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('tasks', {
                    method: 'DELETE',
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        let tasks = this.getLocalData('tasks');
        tasks = tasks.filter(t => t.id !== id);
        this.setLocalData('tasks', tasks);
        return true;
    }

    // ─── Prompts ───

    async getPrompts() {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('prompts', {
                    params: '?order=created_at.desc'
                });
            } catch {
                // fallback
            }
        }
        return this.getLocalData('prompts');
    }

    async createPrompt(prompt) {
        const newPrompt = {
            ...prompt,
            id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
            created_at: new Date().toISOString()
        };

        if (!this.useLocalStorage) {
            try {
                const result = await this.supabaseFetch('prompts', {
                    method: 'POST',
                    body: newPrompt
                });
                return result[0] || newPrompt;
            } catch {
                // fallback
            }
        }

        const prompts = this.getLocalData('prompts');
        prompts.push(newPrompt);
        this.setLocalData('prompts', prompts);
        this.logActivity('create', 'prompt', newPrompt.titulo);
        return newPrompt;
    }

    async updatePrompt(id, updates) {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('prompts', {
                    method: 'PATCH',
                    body: updates,
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        const prompts = this.getLocalData('prompts');
        const index = prompts.findIndex(p => p.id === id);
        if (index !== -1) {
            prompts[index] = { ...prompts[index], ...updates };
            this.setLocalData('prompts', prompts);
        }
        return prompts[index];
    }

    async deletePrompt(id) {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('prompts', {
                    method: 'DELETE',
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        let prompts = this.getLocalData('prompts');
        prompts = prompts.filter(p => p.id !== id);
        this.setLocalData('prompts', prompts);
        return true;
    }

    // ─── Documents ───

    async getDocs() {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('docs', {
                    params: '?order=created_at.desc'
                });
            } catch {
                // fallback
            }
        }
        return this.getLocalData('docs');
    }

    async createDoc(doc) {
        const newDoc = {
            ...doc,
            id: Date.now().toString(36) + Math.random().toString(36).substr(2, 5),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        };

        if (!this.useLocalStorage) {
            try {
                const result = await this.supabaseFetch('docs', {
                    method: 'POST',
                    body: newDoc
                });
                return result[0] || newDoc;
            } catch {
                // fallback
            }
        }

        const docs = this.getLocalData('docs');
        docs.push(newDoc);
        this.setLocalData('docs', docs);
        this.logActivity('create', 'doc', newDoc.titulo);
        return newDoc;
    }

    async updateDoc(id, updates) {
        updates.updated_at = new Date().toISOString();

        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('docs', {
                    method: 'PATCH',
                    body: updates,
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        const docs = this.getLocalData('docs');
        const index = docs.findIndex(d => d.id === id);
        if (index !== -1) {
            docs[index] = { ...docs[index], ...updates };
            this.setLocalData('docs', docs);
        }
        return docs[index];
    }

    async deleteDoc(id) {
        if (!this.useLocalStorage) {
            try {
                return await this.supabaseFetch('docs', {
                    method: 'DELETE',
                    params: `?id=eq.${id}`
                });
            } catch {
                // fallback
            }
        }

        let docs = this.getLocalData('docs');
        docs = docs.filter(d => d.id !== id);
        this.setLocalData('docs', docs);
        return true;
    }

    // ─── Activity Log ───

    logActivity(action, type, name) {
        const activities = this.getLocalData('activities');
        activities.unshift({
            id: Date.now().toString(36),
            action,
            type,
            name,
            timestamp: new Date().toISOString()
        });
        // Manter apenas últimas 50 atividades
        if (activities.length > 50) activities.length = 50;
        this.setLocalData('activities', activities);
    }

    getActivities() {
        return this.getLocalData('activities');
    }

    // ─── Export / Import ───

    exportAllData() {
        return {
            projects: this.getLocalData('projects'),
            tasks: this.getLocalData('tasks'),
            prompts: this.getLocalData('prompts'),
            docs: this.getLocalData('docs'),
            activities: this.getLocalData('activities'),
            exportedAt: new Date().toISOString(),
            version: '1.0.0'
        };
    }

    importAllData(data) {
        if (data.projects) this.setLocalData('projects', data.projects);
        if (data.tasks) this.setLocalData('tasks', data.tasks);
        if (data.prompts) this.setLocalData('prompts', data.prompts);
        if (data.docs) this.setLocalData('docs', data.docs);
        if (data.activities) this.setLocalData('activities', data.activities);
        return true;
    }
}

// Instância global
const api = new DevAgentAPI();