# StudyForge AI - Smart Content Creator

[![License](https://img.shields.io/badge/License-Comercial-blue.svg)](LICENSE)  
[![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)](https://github.com/Username9898/studyforge-ai)  
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)  
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)

**Criado por:** Roberto Ribeiro  
**GitHub:** [@Username9898](https://github.com/Username9898)  
**Email:** robertojn321@gmail.com

---

## Sobre o Projeto

**StudyForge AI** é uma plataforma inteligente de criação de conteúdo educativo que permite a qualquer pessoa aprender qualquer assunto de forma simples, intuitiva e completamente automatizada.

### Missão

Democratizar o acesso ao conhecimento de qualidade, utilizando inteligência artificial gratuita para gerar materiais de estudo completos, detalhados e passo a passo sobre qualquer tema que o usuário desejar.

---

## Funcionalidades Principais

### 1. Criador de Conteúdo Inteligente
- Seleção livre de temas/cursos
- Geração automática de conteúdo educativo completo
- Estrutura passo a passo detalhada
- Conteúdo adaptativo e personalizado

### 2. IA Gratuita Integrada
- Modelos LLM open source (Llama, Mistral, Gemma via Ollama)
- Zero dependência de APIs pagas
- Processamento 100% local
- Atualizações automáticas da IA

### 3. Sistema de Arquivos Completo
- Upload de materiais complementares
- Download de conteúdo em múltiplos formatos
- Exportação (PDF, DOCX, TXT, JSON)
- Importação de arquivos externos
- Remoção e organização de arquivos

### 4. Auto-Atualização Inteligente
- Melhoria contínua do sistema
- Atualizações automáticas sem perda de dados
- Evolução da qualidade do conteúdo
- Manutenção da essência inicial

### 5. Interface Intuitiva
- Design clean e minimalista
- Navegação simples e direta
- Acessível para qualquer usuário
- Responsivo (desktop, tablet, mobile)

### 6. Exportação e Compartilhamento
- Download de estudos completos
- Compartilhamento via link
- Impressão otimizada
- Backup automático

---

## Stack Tecnológico

### Backend
- **Python 3.11+** com FastAPI
- **PostgreSQL** - Dados estruturados
- **Redis** - Cache e sessões
- **MinIO** - Armazenamento de arquivos
- **Ollama** - IA local gratuita
- **LangChain** - Orquestração de IA
- **Celery** - Tarefas assíncronas
- **Poetry** - Dependências

### Frontend
- **Next.js 14** com React 18
- **TypeScript** - Type safety
- **Tailwind CSS** - Estilização moderna
- **Framer Motion** - Animações suaves
- **React Query** - Estado e cache
- **Zustand** - Gerenciamento de estado

### DevOps
- **Docker** e **Docker Compose**
- **GitHub Actions** - CI/CD
- **Prometheus** - Monitoramento
- **Grafana** - Dashboards

---

## Estrutura do Projeto

```
studyforge-ai/
├── frontend/                 # Next.js App
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
├── backend/                  # FastAPI API
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── Dockerfile
│   └── pyproject.toml
├── ai-engine/               # Motor de IA
│   ├── prompts/             # Templates de prompts
│   ├── generators/          # Geradores de conteúdo
│   └── processors/          # Processamento
├── docker-compose.yml
├── scripts/
│   ├── setup.sh
│   ├── deploy.sh
│   └── update.sh
├── docs/
│   ├── api/
│   ├── legal/
│   └── user-guide/
├── LICENSE.txt
└── README.md
```

---

## Instalação Rápida

### Pré-requisitos
- Docker 24+ e Docker Compose
- Python 3.11+
- Node.js 18+
- Ollama (para IA local)

### Clone e Setup

```bash
# Clone o repositório
git clone https://github.com/Username9898/studyforge-ai.git
cd studyforge-ai

# Copie as variáveis de ambiente
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Suba a stack completa
docker-compose up -d

# Instale dependências
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
```

### Acessar
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Como Usar

1. **Escolha o Tema**: Selecione qualquer assunto que deseja aprender
2. **Personalize**: Defina nível de detalhe, formato e profundidade
3. **Gere**: A IA cria conteúdo completo passo a passo
4. **Estude**: Acesse material didático estruturado
5. **Exporte**: Baixe em PDF, DOCX ou TXT
6. **Importe**: Adicione materiais complementares

---

## Modelo de Negócio

### Licença Comercial

Este software é protegido por **Licença Proprietária Personalizada**.

**Participação nos Lucros:**
- **1% a 10%** sobre receita bruta auferida com uso comercial
- Pagamento mensal automático
- Contrato flexível conforme faturamento

**Contato para Comercialização:**
- Email: robertojn321@gmail.com
- GitHub: https://github.com/Username9898

**Termos Comerciais:**
- Uso educacional gratuito
- Uso comercial mediante contrato
- Royalty automático sobre vendas
- Proteção contra uso não autorizado

---

## Documentação

- **[Guia do Usuário](docs/user-guide/README.md)** - Como usar a plataforma
- **[Documentação da API](docs/api/README.md)** - Endpoints e exemplos
- **[Arquitetura](docs/architecture/README.md)** - Decisões técnicas
- **[Contrato Comercial](docs/legal/COMMERCIAL_AGREEMENT.md)** - Termos de uso comercial
- **[Termos de Uso](docs/legal/TERMS_OF_USE.md)** - Licença e restrições

---

## Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -am 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

---

## Roadmap

- [x] Estrutura base do projeto
- [ ] Motor de IA com Ollama
- [ ] Interface Next.js completa
- [ ] Sistema de arquivos (upload/download)
- [ ] Exportação multi-formato
- [ ] Auto-atualização inteligente
- [ ] Marketplace de templates
- [ ] App mobile (React Native)
- [ ] Plugin para WordPress
- [ ] API pública para desenvolvedores

---

## Contato

**Roberto Ribeiro**  
📧 Email: robertojn321@gmail.com  
🐙 GitHub: https://github.com/Username9898  
💻 Projeto: https://github.com/Username9898/studyforge-ai

---

## Aviso Legal

Este software é propriedade de **Roberto Ribeiro**, protegido por direitos autorais e contrato comercial específico.

- Uso educacional: **GRATUITO**
- Uso comercial: **1% a 10%** sobre lucros (automático)
- Violações: Multas de R$ 100.000 + ações judiciais

**Ao usar este software, você concorda com os termos de licença.**

Última atualização: Janeiro 2025  
Versão: 1.0.0