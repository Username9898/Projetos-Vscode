# AI Services - Dentarium AI Enterprise

Microsserviços de inteligência artificial que compõem a plataforma Dentarium AI Enterprise.

## Visão Geral

Cada módulo de IA é independente, containerizado e escalável, comunicando-se via API REST.

## Arquitetura

```
ai-services/
├── ocr-engine/           # Extração de texto de imagens/PDFs
├── dashboard-engine/     # Geração automática de dashboards
├── spreadsheet-engine/   # Processamento inteligente de planilhas
├── cadcam-engine/        # Processamento CAD/CAM odontológico
├── analytics-engine/     # Analytics, previsões e insights
├── waste-reduction/      # Detecção de desperdícios
└── self-healing/         # Monitoramento e auto-cura
```

## Módulos

### 1. OCR Engine (`ocr-engine/`)

**Funções:**
- OCR automático em imagens e PDFs
- Suporte a múltiplos idiomas (português, inglês)
- Extração estruturada de dados
- Classificação de documentos

**Tecnologias:**
- Tesseract OCR
- EasyOCR
- OpenCV
- PaddleOCR (opcional)

**Porta:** 8001

### 2. Dashboard Engine (`dashboard-engine/`)

**Funções:**
- Geração automática de dashboards
- Seleção inteligente de visualizações
- Otimização de layout
- Exportação em múltiplos formatos

**Tecnologias:**
- Apache ECharts
- Plotly
- Metabase (integração)
- Pandas

**Porta:** 8002

### 3. Spreadsheet Engine (`spreadsheet-engine/`)

**Funções:**
- Preenchimento automático de células vazias
- Classificação e categorização
- Detecção e correção de inconsistências
- Normalização de dados

**Tecnologias:**
- Pandas
- Polars
- DuckDB
- OpenPyXL

**Porta:** 8003

### 4. CAD/CAM Engine (`cadcam-engine/`)

**Funções:**
- Processamento de arquivos STL/PLY/OBJ
- Identificação de caso odontológico
- Segmentação dental automática
- Detecção de falhas
- Geração de coroas, facetas, próteses
- Criação de guias cirúrgicos

**Tecnologias:**
- Open3D
- VTK
- Blender API
- MeshLab

**Porta:** 8004

### 5. Analytics Engine (`analytics-engine/`)

**Funções:**
- Previsões de tendências
- Detecção de anomalias
- Geração de insights automáticos
- Modelos de ML preditivos

**Tecnologias:**
- MLflow
- scikit-learn
- Ollama (LLM local)
- Pandas

**Porta:** 8005

### 6. Waste Reduction Engine (`waste-reduction/`)

**Funções:**
- Detecção de material desperdiçado
- Identificação de tempo perdido
- Análise de retrabalho
- Recomendações de otimização

**Tecnologias:**
- Processamento de séries temporais
- Análise estatística
- LLM para geração de relatórios

**Porta:** 8006

### 7. Self-Healing Monitor (`self-healing/`)

**Funções:**
- Monitoramento de saúde dos serviços
- Detecção automática de falhas
- Reinício de serviços com problemas
- Rollback de deployments
- Recuperação automática

**Tecnologias:**
- Docker SDK
- Prometheus API
- Grafana API
- OpenTelemetry

**Porta:** 8007

## Desenvolvimento

### Pré-requisitos

- Python 3.11+
- Poetry 1.7+
- Docker 24+

### Setup de um Módulo

```bash
# Exemplo para OCR Engine
cd ai-services/ocr-engine

# Instalar dependências
poetry install

# Copiar variáveis
cp .env.example .env

# Executar
uvicorn main:app --reload --port 8001
```

### Testes

```bash
# Testes unitários
poetry run pytest tests/

# Testes de integração
poetry run pytest tests/integration/
```

## Deploy

Cada serviço é deployado via Docker e orquestrado pelo Docker Compose:

```bash
# Build de todos os serviços
docker-compose build

# Deploy
docker-compose up -d
```

## Variáveis de Ambiente

Cada módulo possui suas próprias variáveis. Consulte `.env.example` de cada serviço.

## Monitoramento

- **Métricas:** Prometheus (porta 9090)
- **Dashboards:** Grafana (porta 3001)
- **Logs:** Loki (porta 3100)
- **Tracing:** Jaeger

## Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -am 'Adiciona nova feature'`
4. Push: `git push origin feature/nova-feature`
5. Abra um Pull Request

## Licença

Propriedade de Roberto Ribeiro. Uso comercial sujeito a contrato.

## Contato

**Roberto Ribeiro**
- Email: robertojn321@gmail.com
- GitHub: https://github.com/Username9898