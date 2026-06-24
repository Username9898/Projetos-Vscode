# -*- coding: utf-8 -*-
"""
Upload e gerenciamento de arquivos.
Autor: Roberto Ribeiro
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.config import settings

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload de arquivo genérico."""
    if not any(file.filename.endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido")
    
    # TODO: Implementar upload para MinIO
    return {
        "message": "Arquivo recebido",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size if hasattr(file, 'size') else "unknown",
    }


@router.get("/types/")
async def get_supported_file_types():
    """Lista tipos de arquivo suportados."""
    return {
        "types": settings.ALLOWED_EXTENSIONS,
        "categories": {
            "documentos": [".pdf", ".docx", ".txt", ".xml", ".json"],
            "planilhas": [".csv", ".xlsx", ".xls"],
            "imagens": [".png", ".jpg", ".jpeg", ".gif"],
            "modelos_3d": [".stl", ".ply", ".obj"],
            "imagens_medicas": [".dcm", ".dicom"],
        }
    }