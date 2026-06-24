# Dentarium AI Enterprise

[![License](https://img.shields.io/badge/License-Comercial-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)](https://github.com/Username9898/dentarium-ai-enterprise)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)

## Sobre o Projeto

**Dentarium AI Enterprise** é uma plataforma SaaS open source projetada para automatizar dashboards, processamento de documentos, preenchimento de planilhas e fluxos operacionais em múltiplos setores (odontologia, engenharia, indústria, logística, financeiro, RH e saúde).

### Criado por
**Roberto Ribeiro** - Desenvolvedor e Arquiteto de Soluções

## Funcionalidades Principais

- **Dashboards Automáticos** - Geração de painéis com KPIs, gráficos e alertas em tempo real
- **Ingestão Inteligente de Dados** - Processamento de Excel, CSV, PDF, DOCX, TXT, XML, JSON, Imagens, STL, PLY, OBJ, DICOM
- **OCR Automático** - Extração de dados de documentos escaneados e imagens
- **Inteligência de Planilhas** - Preenchimento automático, classificação e correção de inconsistências
- **Processamento CAD/CAM** - Fluxo completo para próteses dentárias e modelagem 3D
- **Redução de Desperdícios** - Detecção de materiais desperdiçados, tempo perdido e retrabalho
- **Monitoramento Auto-Curador** - Reinício automático de serviços, rollback e recuperação

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                            │
│                    (Kong / Traefik)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
    ┌─────────────────────────────────────────┐
    │          Microservices Layer            │
    ├─────────────────────────────────────────┤
    │  • Dashboard AI Engine                  │
    │  • Spreadsheet Intelligence             │
    │  • OCR AI Engine                        │
    │  • CAD/CAM AI Engine                    │
    │  • Analytics AI Engine                  │
    │  • Waste Reduction Engine               │
    │  • Self-Healing Engine                  │
    └─────────────────────────────────────────┘
                  │
    ┌─────────────────────────────────────────┐
    │         Data & Storage Layer            │
    ├─────────────────────────────────────────┤
    │  • PostgreSQL (Operational Data)        │
    │  • DuckDB (Analytics)                   │
    │  • Object Storage (S3/MinIO)            │
    └─────────────────────────────────────────┘
```

## Módulos

### 1. Data Ingestion AI
Recebe e processa múltiplos formatos de arquivo com OCR automático, normalização e classificação.

### 2. Dashboard AI
Cria dashboards automáticos com KPIs, gráficos e indicadores usando IA generativa.

### 3. Spreadsheet Intelligence
Preenche planilhas automaticamente, detecta colunas, classifica dados e corrige inconsistências.

### 4. Dental CAD/CAM AI
Fluxo completo: scanner intraoral → STL → processamento → coroas, facetas, próteses e guias cirúrgicos.

### 5. Waste Reduction Engine
Detecta desperdício de material, tempo perdido e retrabalho, gerando relatórios inteligentes.

### 6. Self-Healing Monitor
Monitora logs, APIs, banco de dados e containers com ações automáticas de recuperação.

## Stack Tecnológico

### Backend
- **Python 3.11+** com FastAPI
- **PostgreSQL** para dados operacionais
- **DuckDB** para analytics em memória
- **Pandas/Polars** para processamento de dados
- **Apache Airflow** para orquestração

### Frontend
- **Next.js 14** com React 18
- **TypeScript** para type safety
- **Tailwind CSS** para estilização
- **Apache ECharts / Plotly** para visualizações

### IA/ML
- **OpenCV** para processamento de imagem
- **Tesseract OCR** para extração de texto
- **Open3D** para processamento 3D
- **Meta Llama**, **Mistral AI**, **Gemma** (modelos open source)

### DevOps/Monitoramento
- **Docker** e **Kubernetes** para orquestração
- **Prometheus + Grafana** para métricas
- **Loki** para agregação de logs
- **OpenTelemetry** para tracing distribuído
- **Blender API** para modelagem 3D

### Integrações
- **Apache Airflow** - Orquestração de workflows
- **MinIO** - Object storage compatível com S3
- **Redis** - Cache e filas

## Estrutura do Projeto

```
dentarium-ai-enterprise/
├── frontend/                 # Next.js App
├── backend/                  # FastAPI API Gateway
├── ai-services/              # Microsserviços de IA
│   ├── ocr-engine/           # OCR e extração de texto
│   ├── dashboard-engine/     # Geração de dashboards
│   ├── spreadsheet-engine/   # Processamento de planilhas
│   ├── cadcam-engine/        # Processamento CAD/CAM
│   ├── analytics-engine/     # Analytics e ML
│   ├── waste-reduction/      # Detecção de desperdícios
│   └── self-healing/         # Monitoramento e auto-cura
├── docs/                     # Documentação
│   ├── api/                  # Documentação de API
│   ├── legal/                # Termos legais e contratos
│   └── architecture/         # Arquitetura e decisões técnicas
├── docker/                   # Dockerfiles e compose files
├── kubernetes/               # Manifests K8s
├── scripts/                  # Scripts de deploy e migração
└── tests/                    # Testes automatizados
```

## Instalação Rápida

### Pré-requisitos
- Docker 24+ e Docker Compose
- Python 3.11+
- Node.js 18+ e npm/pnpm
- PostgreSQL 15+
- Tesseract OCR

### Clone e Setup

```bash
# Clone o repositório
git clone https://github.com/Username9898/dentarium-ai-enterprise.git
cd dentarium-ai-enterprise

# Copie as variáveis de ambiente
cp .env.example .env

# Suba a stack completa
docker-compose up -d

# Instale dependências
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

## Documentação

- **[Documentação da API](docs/api/README.md)** - Endpoints e exemplos de uso
- **[Arquitetura](docs/architecture/README.md)** - Decisões arquiteturais
- **[Guia de Deploy](docs/deployment.md)** - Como fazer deploy em produção

## Licenciamento e Contrato Comercial

Este software é protegido por **Licença Proprietária Personalizada**.

Para uso comercial, é necessário:
1. Assinatura de Contrato Comercial específico
2. Participação de receita entre **1% e 10%** conforme acordo firmado
3. Acordo de não-exclusividade (opcional)

### Termos de Uso
- ✅ Uso educacional e pesquisa gratuita
- ✅ Open source (código visível)
- ❌ Uso comercial sem contrato = Violação dos direitos autorais
- ❌ Remoção de marcação de crédito = Violação contratual

**Consulte**: [LICENSE.txt](LICENSE.txt) e [COMMERCIAL_AGREEMENT.md](docs/legal/COMMERCIAL_AGREEMENT.md)

## Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -am 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## Testes

```bash
# Backend
pytest tests/

# Frontend
cd frontend && npm test

# E2E
npm run test:e2e
```

## Roadmap

- [x] Estrutura base do projeto
- [x] Arquitetura de microsserviços
- [ ] OCR Engine completo
- [ ] Dashboard AI generativo
- [ ] Spreadsheet Intelligence
- [ ] CAD/CAM Processing
- [ ] Waste Reduction Engine
- [ ] Self-Healing Monitor
- [ ] Kubernetes deployment automatizado
- [ ] Marketplace de plugins

## Contato

**Roberto Ribeiro**
- GitHub: [@Username9898](https://github.com/Username9898)
- Email: robertojn321@gmail.com

---

**Aviso Legal**: O uso deste software para fins comerciais está sujeito a contrato específico. Violações serão processadas judicialmente conforme legislação de propriedade intelectual brasileira e internacional.