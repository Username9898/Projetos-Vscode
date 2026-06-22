# 🏦 Fincare - Gestão Financeira Inteligente

Sistema completo de gestão financeira com integração de Inteligência Artificial via Groq.

## 🛠️ Stack Tecnológico

- **Frontend:** React.js + Vite
- **Backend:** Node.js + Express
- **Banco de Dados:** PostgreSQL
- **Autenticação:** JWT (JSON Web Tokens)
- **Inteligência Artificial:** Groq AI (Modelo: `llama-3.3-70b-versatile`)
- **Infraestrutura:** Docker & Docker Compose

## ⚙️ Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose
- [Git](https://git-scm.com/)
- Node.js 20+ (para desenvolvimento local)

## 🚀 Como rodar o projeto

### Com Docker (recomendado)

```bash
# Clone o repositório
git clone https://github.com/Username9898/Fincare.git
cd Fincare

# Configure as variáveis de ambiente
cp .env.example .env

# Suba os containers
docker-compose up --build
```

### Desenvolvimento Local

```bash
# Terminal 1 - Backend
cd Fincare/backend
npm install
npm run dev

# Terminal 2 - Frontend
cd Fincare/frontend
npm install
npm run dev
```

### Acessar a aplicação

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:3000
- **Health Check:** http://localhost:3000/api/health

## 🧠 Integração Groq AI

A aplicação utiliza o modelo `llama-3.3-70b-versatile` da Groq para funcionalidades de IA.

### Testar a IA

```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Qual é a capital do Brasil?"}'
```

## 🔐 Autenticação

### Registrar usuário
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Seu Nome","email":"email@exemplo.com","password":"123456"}'
```

### Login
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"email@exemplo.com","password":"123456"}'
```

## 📁 Estrutura do Projeto

```
Fincare/
├── frontend/           # React + Vite
│   ├── src/
│   │   ├── components/ # Componentes React
│   │   ├── api.js      # Configuração axios
│   │   ├── App.jsx     # Componente principal
│   │   ├── main.jsx    # Entry point
│   │   └── index.css   # Estilos globais
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── backend/            # Node.js + Express
│   ├── services/       # Serviços (Groq, etc.)
│   ├── middlewares/    # Middlewares (JWT)
│   ├── routes/        # Rotas da API
│   ├── models/        # Modelos do banco
│   ├── index.js       # Servidor principal
│   └── package.json
├── .env.example       # Variáveis de ambiente
├── docker-compose.yml # Orquestração Docker
├── .gitignore
└── README.md
```

## 👤 Autor

**Roberto Ribeiro**
- GitHub: [@Username9898](https://github.com/Username9898)

## 📄 Licença

Este projeto está sob a licença MIT.