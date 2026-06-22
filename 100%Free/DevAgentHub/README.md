# DevAgent Hub - Painel de Controle

> **Desenvolvido por Roberto Ribeiro (RR98)**

## 📋 Sobre o Projeto

O **DevAgent Hub** é um painel de controle completo para gerenciamento de projetos, tarefas e documentação de desenvolvimento. Desenvolvido com tecnologias web modernas e design responsivo.

## ✨ Funcionalidades

### 🎯 Dashboard
- Visão geral com estatísticas
- Projetos ativos, tarefas pendentes, prompts salvos e documentos
- Últimas atividades registradas
- Ações rápidas para criar novos itens

### 📁 Projetos
- Cadastro de projetos com nome, descrição, status e tecnologias
- Filtros por busca textual e status
- Ações: editar e excluir
- Status: Ativo, Pausado, Concluído, Arquivado

### ✅ Tarefas (Kanban)
- Quadro Kanban com 3 colunas:
  - **A Fazer** (todo)
  - **Fazendo** (doing)
  - **Concluído** (done)
- Drag & drop para mover tarefas entre colunas
- Prioridades: Baixa, Média, Alta
- Contador de tarefas por coluna

### 💬 Biblioteca de Prompts
- Organize prompts por categorias:
  - Desenvolvimento
  - Arquitetura
  - Banco de Dados
  - Frontend
  - Backend
  - Deploy
- Copie prompts com um clique
- Visualização completa do prompt
- Filtros por busca e categoria

### 📚 Documentação
- Tipos de documentos:
  - Nota
  - Tutorial
  - Ideia
  - Documentação
- Busca e filtros avançados
- Editor completo com modais
- Ícones específicos por tipo

### 👤 Sobre
- Perfil do desenvolvedor: **Roberto Ribeiro (RR98)**
- Descrição profissional
- Stack de tecnologias dominadas

## 🚀 Como Usar

### Requisitos
- Navegador moderno (Chrome, Firefox, Edge)
- Conexão com internet (para carregar ícones Font Awesome)
- JavaScript habilitado

### Instalação

1. Clone o repositório ou baixe os arquivos
2. Abra o arquivo `index.html` no navegador
3. Configure o Supabase (opcional) para persistência na nuvem
4. Ou use o modo local (dados salvos no navegador)

### Configuração do Supabase (Opcional)

1. Acesse a página **Configurações**
2. Insira a URL do seu projeto Supabase
3. Cole a Anon Key
4. Clique em "Salvar & Conectar"

### Uso Offline

- Os dados são salvos automaticamente no `localStorage` do navegador
- Exporte dados em JSON para backup
- Importe dados de backups anteriores

## 🛠️ Tecnologias

- **HTML5** - Estrutura
- **CSS3** - Estilização
- **JavaScript (Vanilla)** - Lógica e interatividade
- **Font Awesome 6.5** - Ícones
- **Supabase** - Backend opcional (nuvem)

## 📦 Estrutura do Projeto

```
100%Free/DevAgentHub/
├── index.html          # Página principal
├── css/
│   └── style.css       # Estilos globais
├── js/
│   ├── app.js          # Lógica principal da aplicação
│   └── api.js          # Integração com Supabase/API
└── database/
    └── schema.sql      # Schema do banco de dados
```

## 🎨 Interface

- Design dark mode (padrão)
- Opção de tema claro
- Responsivo para mobile e desktop
- Sidebar colapsável
- Sistema de toasts para notificações
- Modais dinâmicos
- Drag & drop no Kanban

## 📊 Funcionalidades Principais

1. **CRUD Completo** - Criar, ler, atualizar e excluir projetos, tarefas, prompts e documentos
2. **Filtros Inteligentes** - Busca em tempo real em todas as seções
3. **Persistência** - Dados salvos localmente ou na nuvem (Supabase)
4. **Exportação/Importação** - Backup completo dos dados em JSON
5. **Prompt Mestre** - Prompt mestre de arquitetura copiável
6. **Ações Rápidas** - Acesso rápido às funções principais
7. **Histórico** - Registro de atividades recentes

## 🔧 Personalização

### Cores do Tema
- **Primária**: Roxo (#7c3aed)
- **Sucesso**: Verde (#00e676)
- **Info**: Azul (#00d4ff)
- **Aviso**: Amarelo (#ffab00)
- **Perigo**: Vermelho (#ff1744)

### Ícones
- Font Awesome 6.5.1
- Ícones contextuais por seção
- Animações suaves

## 📝 Notas de Versão

### v1.1.0
- Adicionada página "Sobre" com perfil do desenvolvedor
- Melhorias no footer com branding RR98
- Status de conexão online
- Atualização de versão

### v1.0.0
- Lançamento inicial
- Dashboard, Projetos, Tarefas, Prompts e Documentação
- Integração com Supabase
- Sistema de export/import
- Modo escuro/claro

## 👨‍💻 Autor

**Roberto Ribeiro** - RR98

- Desenvolvedor Full Stack
- Especialista em JavaScript, Node.js, React
- Apaixonado por criar soluções inovadoras

## 📄 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Compartilhar o projeto

## � Contato

Para entrar em contato, utilize os canais oficiais do projeto.

---

**Última atualização:** Junho 2026  
**Versão:** 1.1.0  
**Desenvolvido com ❤️ por RR98**