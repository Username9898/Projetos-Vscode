# -*- coding: utf-8 -*-
"""
OCR AI Engine endpoints.
Autor: Roberto Ribeiro
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.config import settings

router = APIRouter()


@router.post("/process-image/")
async def process_image_ocr(file: UploadFile = File(...)):
    """Processa imagem com OCR."""
    if not settings.ENABLE_OCR:
        raise HTTPException(status_code=503, detail="OCR desabilitado")
    
    # TODO: Integrar com OCR AI Engine
    return {
        "status": "processed",
        "text_extracted": "Exemplo de texto extraído...",
        "confidence": 0.95,
        "language": "por+eng",
    }


@router.post("/process-pdf/")
async def process_pdf_ocr(file: UploadFile = File(...)):
    """Processa PDF com OCR."""
    if not settings.ENABLE_OCR:
        raise HTTPException(status_code=503, detail="OCR desabilitado")
    
    # TODO: Integrar com OCR AI Engine
    return {
        "status": "processed",
        "pages": 5,
        "text_extracted": "Texto extraído do PDF...",
        "confidence": 0.92,
    }