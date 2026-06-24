# -*- coding: utf-8 -*-
"""
API Router - Agrega todas as rotas da API v1
Autor: Roberto Ribeiro
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    health,
    files,
    ocr,
    dashboards,
    spreadsheets,
    cadcam,
    analytics,
    waste,
    monitoring,
)

api_router = APIRouter()

# Incluir todos os endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["autenticacao"])
api_router.include_router(users.router, prefix="/users", tags=["usuarios"])
api_router.include_router(health.router, prefix="/health", tags=["saude"])
api_router.include_router(files.router, prefix="/files", tags=["arquivos"])
api_router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
api_router.include_router(dashboards.router, prefix="/dashboards", tags=["dashboards"])
api_router.include_router(spreadsheets.router, prefix="/spreadsheets", tags=["planilhas"])
api_router.include_router(cadcam.router, prefix="/cadcam", tags=["cadcam"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(waste.router, prefix="/waste", tags=["desperdicio"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoramento"])