from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from loguru import logger

from app.core.config import settings
from app.db.session import engine, async_session
from app.models import Base
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de startup e shutdown."""
    # Startup
    logger.info("Iniciando StudyForge AI Backend...")
    
    # Criar tabelas do banco de dados
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Banco de dados inicializado")
    logger.info("StudyForge AI Backend rodando!")
    
    yield
    
    # Shutdown
    logger.info("Encerrando StudyForge AI Backend...")


app = FastAPI(
    title="StudyForge AI API",
    description="API para plataforma de criação de conteúdo educativo",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "message": "StudyForge AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "studyforge-backend"
    }