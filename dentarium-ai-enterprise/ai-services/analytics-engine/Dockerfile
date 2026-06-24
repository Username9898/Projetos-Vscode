# Analytics AI Engine
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry==1.7.1

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-interaction --no-ansi

COPY . .

ENV DATABASE_URL=postgresql://dentarium:dentarium2025secure@postgres:5432/dentarium_ai
ENV REDIS_URL=redis://:redis2025@redis:6379/5
ENV OLLAMA_HOST=http://ollama:11434
ENV MLFLOW_TRACKING_URI=http://mlflow:5000

EXPOSE 8005

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "2"]