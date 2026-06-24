# -*- coding: utf-8 -*-
"""
Sessão do banco de dados SQLAlchemy.
Autor: Roberto Ribeiro
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

from app.config import settings

# Motor de banco de dados assíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
    poolclass=NullPool if settings.ENVIRONMENT == "testing" else None,
)

# SessionLocal assíncrono
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base para modelos ORM
Base = declarative_base()


# Dependency para FastAPI
async def get_db() -> AsyncSession:
    """
    Dependency que fornece uma sessão de banco de dados.
    Usado com Depends() nos endpoints.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()