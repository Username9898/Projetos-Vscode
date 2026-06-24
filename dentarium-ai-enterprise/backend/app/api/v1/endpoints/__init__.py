# -*- coding: utf-8 -*-
"""
Módulo de endpoints da API.
Autor: Roberto Ribeiro
"""

from app.api.v1.endpoints import (
    auth,
    users,
    health,
    files,
)

__all__ = ["auth", "users", "health", "files"]