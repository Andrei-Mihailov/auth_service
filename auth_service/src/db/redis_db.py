import json

from typing import Union

import backoff
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as conn_err_redis

from .cache import Cache


CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class RedisCache(Cache):
    def __init__(self):
        self.redis: Union[Redis, None]

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def get(self, key) -> Union[bytes, None]:
        data = await self.redis.get(key)
        if not data:
            return None
        return data

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def set(self, key, value, expire=None):
        await self.redis.set(key, value)
        if expire:
            await self.redis.expire(key, expire)

    async def set_jwt(self, token_type, user_id, token, expire=None):
        key = f"jwt_tokens:{token_type}:{user_id}"
        await self.set(key, token, expire)

    async def get_jwt(self, token_type, user_id):
        key = f"jwt_tokens:{token_type}:{user_id}"
        await self.get(key)

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def set_array(self, key, array):
        await self.redis.lpush(key, *array)

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def get_array(self, key):
        array = await self.redis.lrange(key, 0, -1)
        return array

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def set_user_hash(self, user_id, user_data):
        # user_data = json.dumps({'role': role_id,
        #                         'username': user_name,
        #                         'first_name': first_name,
        #                         "last_name": last_name,
        #                         "created_at": created_at})
        await self.redis.hset('users', f"{user_id}", user_data)

    @backoff.on_exception(backoff.expo, conn_err_redis, max_tries=5)
    async def get_user_hash(self, user_id):
        info: bytes = await self.redis.hget('users', user_id)
        return json.loads(info.decode())


redis: Union[RedisCache, None] = None


async def get_redis() -> RedisCache:
    return redis
