# Multi-stage build para otimização
FROM python:3.11-slim-bullseye AS builder

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar Poetry
ENV POETRY_VERSION=1.7.1
RUN pip install poetry==$POETRY_VERSION

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Stage final
FROM python:3.11-slim-bullseye

# Instalar curl e libpq
RUN apt-get update && apt-get install -y \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar dependências do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini ./

# Criar diretórios necessários
RUN mkdir -p uploads exports logs

# Expor porta
EXPOSE 8000

# Variáveis de ambiente padrão
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]