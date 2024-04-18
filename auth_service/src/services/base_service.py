from abc import ABC, abstractmethod
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from uuid import UUID

from db.redis_db import RedisCache
from db.postgres_db import PostgresDatabase, AsyncSession
from models.entity import User
CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class AbstractBaseService(ABC):
    pass
    # @abstractmethod
    # async def get_by_id(self, id):
    #     pass

    # @abstractmethod
    # async def _get_from_db(self, id):
    #     pass

    # @abstractmethod
    # async def _get_from_cache(self, key):
    #     pass

    # @abstractmethod
    # async def _put_to_cache(self, key, value, expire):
    #     pass

    # @abstractmethod
    # async def execute_query_storage(self, query):
    #     pass


class BaseService(AbstractBaseService):
    def __init__(self, cache: RedisCache, storage: AsyncSession):
        self.cache = cache
        self.storage = storage

    async def create_new_user(self, user_params):
        user_dto = jsonable_encoder(user_params)
        user = User(**user_dto)
        self.storage.add(user)
        try:
            await self.storage.commit()
        except Exception as e:
            return None
        await self.storage.refresh(user)
        return user

    async def get_user_by_login(self, login):
        stmt = select(User).filter(User.login == login)
        # Выполняем запрос с помощью метода execute
        result = await self.storage.execute(stmt)
        # Получаем первую запись из результата
        user = result.scalars().first()
        return user

    async def del_user_by_id(self, id: UUID):
        async with self.storage() as session:
            user = await session.get(User, id)
            if user:
                session.delete(user)
                await session.commit()
                return True
            else:
                return False
