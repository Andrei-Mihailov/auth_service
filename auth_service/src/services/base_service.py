import backoff
import json

from abc import ABC, abstractmethod
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from typing import Union


from redis.exceptions import ConnectionError as conn_err_redis
from asyncpg.exceptions import PostgresConnectionError as conn_err_pg
from db.redis_db import RedisCache
from db.postgres_db import AsyncSession
from models.entity import User, Authentication
from core.config import settings
from services.utils import decode_jwt


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
        self.model = None

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def create_new_instance(self, model_params):
        if not isinstance(model_params, dict):
            models_dto = jsonable_encoder(model_params)
        else:
            models_dto = model_params
        instance = self.model(**models_dto)
        self.storage.add(instance)
        try:
            await self.storage.commit()
        except Exception as e:
            print(f"Ошибка при создании объекта: {e}")
            return None
        await self.storage.refresh(instance)
        return instance

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def change_instance_data(self, instance_id: int, model_params: dict):
        try:
            instance = await self.storage.get(self.model, instance_id)
            if instance is None:
                return None

            if not isinstance(model_params, dict):
                updated_data = jsonable_encoder(model_params)
            else:
                updated_data = model_params

            for field, value in updated_data.items():
                if field in ['login', 'password'] and value is None:
                    continue
                setattr(instance, field, value)

            await self.storage.commit()
            await self.storage.refresh(instance)
            return instance
        except Exception as e:
            print(f"Ошибка при обновлении объекта: {e}")
            return None

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def get_user_by_login(self, login):
        stmt = select(User).filter(User.login == login)
        result = await self.storage.execute(stmt)
        user = result.scalars().first()
        return user

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def get_instance_by_id(self, id: str):
        stmt = select(self.model).filter(self.model.id == id)
        result = await self.storage.execute(stmt)
        instance = result.scalars().first()
        return instance

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def get_instance_by_name(self, name: str):
        stmt = select(self.model).filter(self.model.name == name)
        result = await self.storage.execute(stmt)
        instance = result.scalars().first()
        return instance

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def del_instance_by_id(self, id: str):
        instance = await self.storage.get(self.model, id)
        if instance:
            await self.storage.delete(instance)
            await self.storage.commit()
            return True
        else:
            return False

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def get_all_instance(self):
        stmt = select(self.model)
        result = await self.storage.execute(stmt)
        instance = result.scalars().all()
        return instance

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def get_login_history(self, user_uuid: str):
        user = await self.storage.get(User, user_uuid)
        if user is None:
            return None
        stmt = select(self.model).filter(self.model.user_id == user_uuid)
        result = await self.storage.execute(stmt)
        instance = result.scalars().all()
        return instance

    @backoff.on_exception(backoff.expo, conn_err_pg, max_tries=5)
    async def set_user_role(self, instance: User, role):
        instance.role = role
        await self.storage.commit()
        await self.storage.refresh(instance)
        return instance

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def _put_to_cache(
            self,
            key: Union[dict, str],
            value: Union[User, Authentication, dict, list[dict]],
            expire: int):
        await self.cache.set(key if isinstance(key, str) else json.dumps(key),
                             value.json() if isinstance(value, self.model) else json.dumps(value),
                             expire)

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def _delete_from_cache(
        self,
        key: Union[dict, str]
    ):
        try:
            await self.cache.delete(key if isinstance(key, str) else json.dumps(key))
        except Exception as e:
            print(f"Ошибка при удалении из кэша: {e}")

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def _get_from_cache(self, key: Union[dict, str]) -> Union[User, Authentication, None]:
        data = await self.cache.get(json.dumps(key) if isinstance(key, dict) else key)
        if not data:
            return None

        instance_data = json.loads(data)
        if instance_data:
            if isinstance(instance_data, list) | isinstance(instance_data, str):
                return instance_data
            else:
                instance_data = self.model(**instance_data)
        return instance_data

    async def add_to_white_list(self, token, token_type):
        payload = decode_jwt(jwt_token=token)
        key = "white_list:" + payload.get("self_uuid")
        if token_type == 'refresh':
            expire = settings.auth_jwt.refresh_token_expire_minutes
        else:
            expire = settings.auth_jwt.access_token_expire_minutes
        await self._put_to_cache(key, token, expire)

    async def get_from_white_list(self, token):
        payload = decode_jwt(jwt_token=token)
        key = "white_list:" + payload.get("self_uuid")
        return await self._get_from_cache(key)

    async def del_from_white_list(self, token):
        payload = decode_jwt(jwt_token=token)
        key = "white_list:" + payload.get("self_uuid")
        await self._delete_from_cache(key)

    async def add_to_black_list(self, token, token_type):
        payload = decode_jwt(jwt_token=token)
        key = "black_list:" + payload.get("self_uuid")
        if token_type == 'refresh':
            expire = settings.auth_jwt.refresh_token_expire_minutes
        else:
            expire = settings.auth_jwt.access_token_expire_minutes
        await self._put_to_cache(key, token, expire)

    async def get_from_black_list(self, token):
        payload = decode_jwt(jwt_token=token)
        key = "black_list:" + payload.get("self_uuid")
        return await self._get_from_cache(key)
