# CAD/CAM AI Engine
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    libopencv-dev \
    libgl1 \
    libglib2.0-0 \
    meshlab \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry==1.7.1

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-interaction --no-ansi

COPY . .

ENV DATABASE_URL=postgresql://dentarium:dentarium2025secure@postgres:5432/dentarium_ai
ENV REDIS_URL=redis://:redis2025@redis:6379/4
ENV MINIO_ENDPOINT=minio:9000
ENV BLENDER_PATH=/usr/bin/blender

EXPOSE 8004

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004", "--workers", "2"]