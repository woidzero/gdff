import asyncio
from typing import Annotated, TypeAlias

from sqlalchemy import BigInteger, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, registry

from src.config import Config

from .util import SingletonMeta

Int16: TypeAlias = Annotated[int, 16]
Int64: TypeAlias = Annotated[int, 64]


class Base(AsyncAttrs, DeclarativeBase):
    registry = registry(type_annotation_map={Int16: Integer, Int64: BigInteger})


class Database(metaclass=SingletonMeta):
    BASE = Base

    def __init__(self):
        self._engine: AsyncEngine = create_async_engine(f"sqlite+aiosqlite:///{Config.DB_FILE}")
        session = async_sessionmaker(bind=self._engine, expire_on_commit=False)
        self._session: AsyncSession = session()

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    def engine(self) -> AsyncEngine:
        return self._engine


async def register_models() -> None:
    async with Database().engine.begin() as conn:
        await conn.run_sync(Database.BASE.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(register_models())
