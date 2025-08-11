from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os
from typing import AsyncGenerator

DATABASE_URL_PROD = "sqlite+aiosqlite:///products.db"
DATABASE_URL_USER = "sqlite+aiosqlite:///user.db"

async_engine_prod = create_async_engine(
    url=DATABASE_URL_PROD,
    echo=True,
)
async_engine_user = create_async_engine(
    url=DATABASE_URL_USER,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine_prod)
async_session_user = async_sessionmaker(async_engine_user)


async def get_prod_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()  
            raise
        finally:
            await session.close()

async def get_user_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_user() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()