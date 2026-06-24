# OCR AI Engine
FROM python:3.11-slim

# Instalar dependências do sistema incluindo Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    libtesseract-dev \
    libopencv-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar Poetry
RUN pip install poetry==1.7.1

# Copiar dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-interaction --no-ansi

# Copiar código
COPY . .

# Variável de ambiente para Tesseract
ENV TESSERACT_CMD=/usr/bin/tesseract
ENV OLLAMA_HOST=http://ollama:11434

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]