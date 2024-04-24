import backoff
from asyncpg.exceptions import PostgresConnectionError as conn_err
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import pg_config_data

Base = declarative_base()
dsn = (
    f"postgresql+asyncpg://{pg_config_data.user}:{pg_config_data.password}@{pg_config_data.host}:"
    f"{pg_config_data.port}/{pg_config_data.dbname}"
)
engine = create_async_engine(dsn, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@backoff.on_exception(backoff.expo, conn_err, max_tries=5)
async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@backoff.on_exception(backoff.expo, conn_err, max_tries=5)
async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
