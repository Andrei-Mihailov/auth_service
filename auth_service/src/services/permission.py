from functools import lru_cache
from typing import Union
from fastapi import Depends

from .base_service import BaseService
from db.redis_db import RedisCache, get_redis
from db.postgres_db import AsyncSession, get_session


class PermissionService(BaseService):
    pass


@lru_cache()
def get_permission_service(
        redis: RedisCache = Depends(get_redis),
        db: AsyncSession = Depends(get_session),
) -> PermissionService:

    return PermissionService(redis, db)
