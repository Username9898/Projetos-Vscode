from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # App
    APP_NAME: str = "StudyForge AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://studyforge:studyforge123@db:5432/studyforge"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # MinIO
    MINIO_URL: str = "http://minio:9000"
    MINIO_ACCESS_KEY: str = "studyforge"
    MINIO_SECRET_KEY: str = "studyforge123"
    MINIO_BUCKET: str = "studyforge"
    
    # Ollama
    OLLAMA_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama2"
    
    # Security
    SECRET_KEY: str = "studyforge-secret-key-2025"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 dias
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    # Telemetria
    TELEMETRY_ENABLED: bool = True
    TELEMETRY_URL: str = "http://localhost:8000/api/v1/telemetry"
    
    # Licenciamento
    LICENSE_KEY: str = ""
    HARDWARE_ID: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()