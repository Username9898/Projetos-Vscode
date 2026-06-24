# -*- coding: utf-8 -*-
"""
User management endpoints.
Autor: Roberto Ribeiro
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User

router = APIRouter()


@router.get("/")
async def list_users(db: AsyncSession = Depends(get_db)):
    """Lista todos os usuários."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]}


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Obtém usuário específico."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"id": user.id, "username": user.username, "email": user.email}