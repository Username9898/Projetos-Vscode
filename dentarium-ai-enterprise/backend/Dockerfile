# Multi-stage build para produção
FROM python:3.11-slim as builder

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Instalar Poetry
RUN pip install poetry==1.7.1

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Configurar Poetry para instalar no sistema
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-interaction --no-ansi

# ==================== STAGE FINAL ====================
FROM python:3.11-slim as runtime

# Metadados da imagem
LABEL maintainer="Roberto Ribeiro <contato@dentarium-ai.enterprise.com.br>"
LABEL description="Dentarium AI Enterprise - API Gateway"
LABEL version="1.0.0"

# Criar usuário não-root
RUN groupadd -r dentarium && useradd -r -g dentarium dentarium

# Instalar dependências runtime
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências instaladas do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação
COPY --chown=dentarium:dentarium . .

# Mudar para usuário não-root
USER dentarium

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]