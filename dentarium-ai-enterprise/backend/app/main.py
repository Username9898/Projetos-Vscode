# -*- coding: utf-8 -*-
"""
Dentarium AI Enterprise - API Gateway
Main Application Entry Point

Autor: Roberto Ribeiro
Email: contato@dentarium-ai.enterprise.com.br
GitHub: https://github.com/roberto-ribeiro/dentarium-ai-enterprise
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import make_asgi_app
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.config import settings
from app.api.v1.api import api_router
from app.core.logging import setup_logging
from app.db.session import engine
from app.db.base import Base
from app.core.metrics import setup_metrics


# Configurar Sentry para monitoramento de erros (opcional)
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration(auto_enabling_integrations=False)],
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        environment=settings.ENVIRONMENT,
        release=f"dentarium-ai@{settings.VERSION}",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Executado no startup e shutdown.
    """
    # Startup
    setup_logging()
    setup_metrics(app)
    
    # Criar tabelas do banco de dados (apenas para desenvolvimento)
    if settings.ENVIRONMENT != "production":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="Dentarium AI Enterprise API",
    description="API Gateway para plataforma de IA empresarial",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    license_info={
        "name": "Proprietary License - Roberto Ribeiro",
        "url": "https://github.com/roberto-ribeiro/dentarium-ai-enterprise/blob/main/LICENSE.txt",
    },
    contact={
        "name": "Roberto Ribeiro",
        "email": "contato@dentarium-ai.enterprise.com.br",
        "url": "https://github.com/roberto-ribeiro",
    },
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Incluir rotas
app.include_router(api_router, prefix=settings.API_V1_STR)

# Métricas Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint com informações básicas."""
    return {
        "name": "Dentarium AI Enterprise",
        "version": settings.VERSION,
        "status": "running",
        "author": "Roberto Ribeiro",
        "docs": "/docs",
        "redoc": "/redoc",
        "metrics": "/metrics",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "database": "connected",
        "redis": "connected",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info",
    )