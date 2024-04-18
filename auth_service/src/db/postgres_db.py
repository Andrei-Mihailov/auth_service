from typing import Union

import asyncpg
import backoff
from asyncpg.exceptions import UndefinedTableError as undefined_table_err
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .database import Database
from core.config import pg_config_data

Base = declarative_base()
dsn = f'postgresql+asyncpg://{pg_config_data.user}:{pg_config_data.password}@{pg_config_data.host}:{pg_config_data.port}/{pg_config_data.dbname}'
engine = create_async_engine(dsn, echo=True, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class PostgresDatabase(Database):
    def __init__(self):
        self.connection: Union[asyncpg.Connection, None]

    @backoff.on_exception(backoff.expo, undefined_table_err, max_tries=5)
    async def execute_query(self, query, *args) -> Union[asyncpg.Record, None]:
        async with self.connection.transaction():
            return await self.connection.fetchrow(query, *args)

    @backoff.on_exception(backoff.expo, undefined_table_err, max_tries=5)
    async def execute(self, query, *args):
        async with self.connection.transaction():
            return await self.connection.execute(query, *args)


postgres: Union[PostgresDatabase, None] = None


async def get_postgres() -> PostgresDatabase:
    return postgres
