from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import engine, sessionmaker


class BaseRepository:
    def __init__(self):
        self._session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @property
    def session(self):
        return self._session
