# -*- coding: utf-8 -*-
"""
Waste Reduction Engine endpoints.
Autor: Roberto Ribeiro
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class WasteAnalysisRequest(BaseModel):
    process_type: str
    period: str = "last_30_days"


@router.post("/analyze/")
async def analyze_waste(request: WasteAnalysisRequest):
    """Analisa desperdícios no processo."""
    return {
        "waste_detected": [
            {"type": "material", "amount": 15.5, "unit": "kg", "cost": 450.0},
            {"type": "time", "amount": 120, "unit": "minutes", "cost": 800.0},
            {"type": "rework", "amount": 8, "unit": "instances", "cost": 1200.0},
        ],
        "total_cost": 2450.0,
        "savings_potential": 1850.0,
    }


@router.get("/recommendations/")
async def get_recommendations():
    """Retorna recomendações de redução de desperdício."""
    return {
        "recommendations": [
            {"priority": "high", "action": "Otimizar corte de material", "savings": "30%"},
            {"priority": "medium", "action": "Revisar processo de polimento", "savings": "15%"},
            {"priority": "low", "action": "Atualizar treinamento de operadores", "savings": "10%"},
        ]
    }