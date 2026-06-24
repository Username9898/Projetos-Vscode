# -*- coding: utf-8 -*-
"""
Configurações da aplicação usando Pydantic Settings.
Autor: Roberto Ribeiro
"""

from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações globais da aplicação."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )
    
    # Aplicação
    APP_NAME: str = "Dentarium AI Enterprise"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "change-me-in-production-32chars-minimum"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]
    
    # Banco de dados
    DATABASE_URL: str = "postgresql://dentarium:dentarium2025secure@localhost:5432/dentarium_ai"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://:redis2025@localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # MinIO / S3
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin2025"
    MINIO_BUCKET_NAME: str = "dentarium-files"
    MINIO_SECURE: bool = False
    
    # JWT / Autenticação
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # LLM / IA
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Upload
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".docx", ".txt", ".csv", ".xlsx", ".xls",
        ".json", ".xml", ".png", ".jpg", ".jpeg", ".gif",
        ".stl", ".ply", ".obj", ".dcm", ".dicom",
    ]
    
    # Tesseract OCR
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    TESSERACT_LANG: str = "por+eng"
    
    # Email / Notificações
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: str = "Dentarium AI Enterprise"
    
    # Webhooks
    WEBHOOK_SECRET: Optional[str] = None
    
    # Feature Flags
    ENABLE_OCR: bool = True
    ENABLE_CAD_CAM: bool = True
    ENABLE_PREDICTIONS: bool = True
    ENABLE_WASTE_DETECTION: bool = True
    ENABLE_SELF_HEALING: bool = True


settings = Settings()