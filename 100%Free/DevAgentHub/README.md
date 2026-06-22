# 🚀 DevAgent Hub

**Seu quartel-general de desenvolvimento 100% gratuito na nuvem**

Painel web completo para gerenciar projetos, tarefas, prompts de IA e documentação. Funciona 100% no navegador com fallback para localStorage, e opcionalmente pode ser conectado ao Supabase para persistência na nuvem.

## 📋 Funcionalidades

### 📁 Módulo de Projetos
- Criar e gerenciar projetos
- Definir status (Ativo, Pausado, Concluído, Arquivado)
- Registrar tecnologias e links do repositório
- Filtrar e pesquisar projetos

### 📋 Kanban de Tarefas
- Quadro visual no estilo Kanban (A Fazer / Fazendo / Concluído)
- Arrastar e soltar tarefas entre colunas
- Prioridades (Baixa, Média, Alta)
- Visualização detalhada

### 🤖 Biblioteca de Prompts
- Salvar prompts para IA
- Categorias (Desenvolvimento, Arquitetura, Banco de Dados, etc.)
- Copiar com 1 clique
- Busca e filtro por categoria

### 📚 Documentação
- Notas, Tutoriais, Ideias e Documentação
- Editor completo
- Busca por texto

### ⚙️ Configurações
- Conexão com Supabase
- Tema escuro/claro
- Exportar/Importar dados (JSON)

## 🏗️ Arquitetura

```
Você (navegador)
    │
    ├── DevAgent Hub (HTML/CSS/JS)
    │
    ├── Supabase (banco de dados - opcional)
    │
    ├── GitHub (código fonte)
    │
    ├── Cloudflare Pages (hospedagem)
    │
    └── Google AI Studio (IA programadora)
```

## 🚀 Deploy Gratuito (Cloudflare Pages)

### Passo 1 - Criar conta no GitHub
1. Acesse [github.com](https://github.com) e crie sua conta
2. Clique em **New Repository**
3. Nome: `devagent-hub`
4. Marque **Public** ou **Private**
5. Click **Create repository**

### Passo 2 - Enviar o código
```bash
# Clone o repositório
git clone https://github.com/SEU-USUARIO/devagent-hub.git

# Copie os arquivos do DevAgent Hub para dentro da pasta
# (ou faça upload manual pelo site do GitHub)

# Adicione e envie os arquivos
git add .
git commit -m "Initial commit - DevAgent Hub"
git push origin main
```

### Passo 3 - Criar conta no Cloudflare
1. Acesse [cloudflare.com](https://cloudflare.com) e crie sua conta
2. No dashboard, clique em **Pages**
3. Clique em **Create a Project** > **Connect to Git**
4. Autorize o acesso ao GitHub
5. Selecione o repositório `devagent-hub`
6. Configurações:
   - **Project name**: `devagent-hub`
   - **Production branch**: `main`
   - **Build settings**: None (estático)
   - **Build command**: deixe vazio
   - **Build output directory**: deixe vazio
7. Clique **Save and Deploy**

### Passo 4 - Configurar Supabase (opcional)
1. Acesse [supabase.com](https://supabase.com) e crie sua conta
2. Clique em **New Project**
3. Nome: `devagent-hub`
4. Escolha uma região próxima (ex: São Paulo)
5. Salve a **Database Password**
6. Após criar, vá em **SQL Editor**
7. Cole o conteúdo de `database/schema.sql`
8. Execute o SQL
9. Vá em **Settings** > **API**
10. Copie a **URL** e a **anon public key**
11. No DevAgent Hub, vá em **Configurações**
12. Cole a URL e a Key
13. Clique em **Salvar & Conectar**

### Passo 5 - Acessar
- Seu site estará online em: `https://devagent-hub.pages.dev`
- (substitua pelo seu subdomínio real)

## 💻 Como usar

### Fluxo de trabalho diário
1. Abra o DevAgent Hub (Cloudflare Pages)
2. Crie um projeto no módulo **Projetos**
3. Defina as tarefas no **Kanban**
4. Use a **Biblioteca de Prompts** para salvar prompts para IA
5. Copie o **Prompt Mestre** no Dashboard
6. Cole no [Google AI Studio](https://aistudio.google.com)
7. Receba o código gerado
8. Salve no GitHub
9. Publique no Cloudflare Pages
10. Registre a documentação

## 🧠 Prompt Mestre

```text
Você é meu arquiteto de software e desenvolvedor full stack.

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

Sempre entregue código completo e funcional.
```

## 📁 Estrutura do Projeto

```
DevAgentHub/
├── index.html          # Página principal
├── css/
│   └── style.css       # Estilos completos
├── js/
│   ├── api.js          # API service (Supabase + localStorage)
│   └── app.js          # Lógica principal do app
├── database/
│   └── schema.sql      # Schema do Supabase
└── README.md           # Esta documentação
```

## 🔧 Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Ícones**: Font Awesome 6
- **Banco**: Supabase (PostgreSQL) ou localStorage
- **Hospedagem**: Cloudflare Pages (gratuita)
- **Editor**: VS Code Web / Qualquer editor

## ⚠️ Limitações dos Planos Gratuitos

| Serviço | Limitação |
|---------|-----------|
| Cloudflare Pages | Sites ilimitados, 500 builds/mês, 1GB storage |
| Supabase | 500MB database, 2GB bandwidth, 50,000 rows |
| GitHub | Repositórios ilimitados (públicos/privados) |
| Google AI Studio | Uso gratuito com limites, modelos poderosos |

## 📦 Exportar / Importar Dados

Para migrar seus dados entre dispositivos ou fazer backup:

1. Vá em **Configurações**
2. Clique em **Exportar Todos os Dados**
3. Salve o arquivo `.json`
4. Em outro dispositivo, vá em **Configurações**
5. Clique em **Importar Dados**
6. Selecione o arquivo

## 🎯 Roadmap

- [x] Dashboard com estatísticas
- [x] CRUD de Projetos
- [x] Kanban de Tarefas com Drag & Drop
- [x] Biblioteca de Prompts
- [x] Documentação
- [x] Tema escuro/claro
- [x] Export/Import de dados
- [ ] Autenticação de usuários
- [ ] Integração direta com APIs de IA
- [ ] Histórico de versões de projetos
- [ ] Compartilhamento de projetos

## 📝 Licença

MIT - Use, modifique e distribua livremente.

---

**Feito com ❤️ para desenvolvedores que querem criar sem gastar nada**