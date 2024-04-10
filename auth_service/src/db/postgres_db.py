from typing import Union

import asyncpg
import backoff
from asyncpg.exceptions import UndefinedTableError as undefined_table_err

from .database import Database


class PostgresDatabase(Database):
    def __init__(self):
        self.connection: Union[asyncpg.Connection, None]

    @backoff.on_exception(backoff.expo, undefined_table_err, max_tries=5)
    async def execute_query(self, query, *args) -> Union[asyncpg.Record, None]:
        async with self.connection.transaction():
            result = await self.connection.fetchrow(query, *args)
            return result

    @backoff.on_exception(backoff.expo, undefined_table_err, max_tries=5)
    async def execute(self, query, *args):
        async with self.connection.transaction():
            await self.connection.execute(query, *args)


postgres: Union[PostgresDatabase, None] = None


async def get_postgres() -> PostgresDatabase:
    return postgres
