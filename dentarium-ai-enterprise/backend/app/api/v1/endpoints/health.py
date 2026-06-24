# -*- coding: utf-8 -*-
"""
Health check endpoints.
Autor: Roberto Ribeiro
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_db
from app.config import settings

router = APIRouter()


@router.get("/")
async def health_check():
    """Health check básico."""
    return {
        "status": "healthy",
        "service": "Dentarium AI Enterprise API",
        "version": settings.VERSION,
        "author": "Roberto Ribeiro",
    }


@router.get("/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Health check detalhado com verificação de dependências."""
    health_status = {
        "status": "healthy",
        "service": "Dentarium AI Enterprise API",
        "version": settings.VERSION,
        "checks": {},
    }
    
    # Verificar banco de dados
    try:
        await db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Verificar Redis (será implementado)
    health_status["checks"]["redis"] = "not_configured"
    
    # Verificar MinIO (será implementado)
    health_status["checks"]["minio"] = "not_configured"
    
    return health_status