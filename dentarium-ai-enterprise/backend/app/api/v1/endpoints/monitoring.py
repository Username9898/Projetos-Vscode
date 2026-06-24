# -*- coding: utf-8 -*-
"""
Self-Healing Monitor endpoints.
Autor: Roberto Ribeiro
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ServiceStatus(BaseModel):
    service: str
    status: str
    uptime: float
    last_check: str


class Alert(BaseModel):
    id: str
    severity: str
    message: str
    timestamp: str
    resolved: bool


@router.get("/services/")
async def get_services_status():
    """Retorna status de todos os serviços."""
    return {
        "services": [
            ServiceStatus(
                service="api-gateway",
                status="healthy",
                uptime=99.9,
                last_check="2025-01-01T12:00:00",
            ),
            ServiceStatus(
                service="ocr-engine",
                status="healthy",
                uptime=99.5,
                last_check="2025-01-01T12:00:00",
            ),
        ]
    }


@router.get("/alerts/")
async def get_active_alerts():
    """Retorna alertas ativos."""
    return {
        "alerts": [
            Alert(
                id="alert_123",
                severity="warning",
                message="Alto uso de memória no serviço X",
                timestamp="2025-01-01T11:55:00",
                resolved=False,
            )
        ]
    }


@router.post("/restart/{service_name}")
async def restart_service(service_name: str):
    """Reinicia um serviço com problemas."""
    return {"status": "restarted", "service": service_name}