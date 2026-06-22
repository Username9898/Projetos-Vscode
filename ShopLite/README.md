# 🛒 ShopLite - E-commerce Inteligente

Plataforma completa de e-commerce com integração de Inteligência Artificial via Groq.

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

## 🚀 Como rodar o projeto

```bash
git clone https://github.com/Username9898/ShopLite.git
cd ShopLite
cp .env.example .env
docker-compose up --build
```

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:3000

## 🧠 Integração Groq AI

```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Recomende produtos para um cliente que gosta de tecnologia"}'
```

## 👤 Autor

**Roberto Ribeiro** - [@Username9898](https://github.com/Username9898)