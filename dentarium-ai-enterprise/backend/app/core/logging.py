# -*- coding: utf-8 -*-
"""
Configuração de logging da aplicação.
Autor: Roberto Ribeiro
"""

import logging
import sys
from pathlib import Path
from loguru import logger

def setup_logging():
    """Configura logging com Loguru."""
    
    # Remover handler padrão
    logger.remove()
    
    # Formato customizado
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # Console handler
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True,
    )
    
    # File handler para erros
    log_path = Path("/app/logs") if Path("/app/logs").exists() else Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / "error.log",
        format=log_format,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        encoding="utf-8",
    )
    
    # File handler para todos os logs
    logger.add(
        log_path / "app.log",
        format=log_format,
        level="DEBUG",
        rotation="50 MB",
        retention="7 days",
        encoding="utf-8",
    )
    
    logger.info("Logging configurado com sucesso")