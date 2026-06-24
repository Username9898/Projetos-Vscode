# Backend - Dentarium AI Enterprise

API Gateway desenvolvida com FastAPI para a plataforma Dentarium AI Enterprise.

## Sobre

Este módulo é o coração do sistema, responsável por:
- Receber requisições de todos os módulos de IA
- Autenticação e autorização de usuários
- Orquestração de serviços
- Gestão de arquivos e dados
- Monitoramento e métricas

## Stack

- **FastAPI** - Framework web de alta performance
- **SQLAlchemy** - ORM assíncrono
- **PostgreSQL** - Banco de dados principal
- **Redis** - Cache e filas
- **MinIO** - Armazenamento de objetos (S3 compatível)
- **Poetry** - Gerenciamento de dependências

## Estrutura

```
backend/
├── app/
│   ├── api/v1/
│   │   └── endpoints/     # Rotas da API
│   ├── core/              # Configurações centrais
│   ├── db/                # Conexões e sessões
│   └── models/            # Modelos ORM
├── pyproject.toml         # Dependências Poetry
├── Dockerfile            # Imagem Docker
└── .env.example          # Variáveis de ambiente
```

## Desenvolvimento

### Pré-requisitos

- Python 3.11+
- Poetry 1.7+
- PostgreSQL 15+
- Redis 7+

### Setup Local

```bash
# Instalar dependências
poetry install

# Copiar variáveis de ambiente
cp .env.example .env

# Executar migrations (quando implementado)
poetry run alembic upgrade head

# Iniciar servidor
poetry run uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

### Endpoints Principais

- `/api/v1/auth/token` - Login e obtenção de JWT
- `/api/v1/health/` - Health check
- `/api/v1/files/upload/` - Upload de arquivos
- `/api/v1/ocr/process-image/` - Processamento OCR
- `/api/v1/dashboards/generate/` - Geração de dashboards
- `/api/v1/spreadsheets/process/` - Processamento de planilhas
- `/api/v1/cadcam/process-stl/` - Processamento CAD/CAM
- `/api/v1/analytics/predict/` - Analytics e previsões
- `/api/v1/waste/analyze/` - Análise de desperdícios
- `/api/v1/monitoring/services/` - Monitoramento

## Docker

```bash
# Build da imagem
docker build -t dentarium-backend .

# Executar container
docker run -p 8000:8000 --env-file .env dentarium-backend
```

## Testes

```bash
# Executar todos os testes
poetry run pytest tests/ -v

# Com coverage
poetry run pytest tests/ --cov=app
```

## Variáveis de Ambiente

Consulte `.env.example` para a lista completa de variáveis.

## Licença

Este software é proprietário. Veja [LICENSE.txt](../../LICENSE.txt) para detalhes.

## Contato

**Roberto Ribeiro**
- Email: robertojn321@gmail.com
- GitHub: https://github.com/Username9898

Última atualização: Janeiro 2025