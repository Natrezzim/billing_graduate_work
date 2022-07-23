import socket

import asyncpg
import backoff
from sqlmodel import SQLModel

from app.core.config import Settings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

settings = Settings()

DATABASE_URL = f'postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}' \
               f':{settings.db_port}/{settings.db_name}'

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(ConnectionRefusedError, socket.gaierror, asyncpg.InvalidCatalogNameError))
async def test_connection():
    conn = await engine.connect()
    await conn.execute(select(1))
    await conn.close()
