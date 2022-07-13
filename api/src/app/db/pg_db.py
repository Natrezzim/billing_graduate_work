import socket

import backoff
from app.core.config import Settings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

settings = Settings()

DATABASE_URL = f'postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}' \
               f':{settings.db_port}/{settings.db_name}'

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(ConnectionRefusedError, socket.gaierror))
async def test_connection():
    conn = await engine.connect()
    await conn.execute(select(1))
    await conn.close()
