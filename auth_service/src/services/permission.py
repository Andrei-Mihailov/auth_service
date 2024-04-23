from fastapi import Depends, HTTPException, status
from functools import lru_cache

from models.entity import Permissions
from .base_service import BaseService
from db.redis_db import RedisCache, get_redis
from db.postgres_db import AsyncSession, get_session
from service.base_service import has_permision


class PermissionService(BaseService):
    def __init__(self, cache: RedisCache, storage: AsyncSession):
        super().__init__(cache, storage)
        self.model = Permissions

    async def create_permission(self, params: dict, access_token: str) -> Permissions:
        if has_permision(access_token) == 2 or has_permision(access_token) == 1:
            permission = await self.create_new_instance(params)
            return permission
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are not superuser",
            )

    async def assign_permission_to_role(self, data: dict, access_token: str) -> bool:
        if has_permision(access_token) == 2:
            role = await self.permission_to_role(
                str(data.permissions_id), str(data.role_id)
            )
            if role is not None:
                return True
            else:
                return False
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are not admin user",
            )

    async def remove_permission_from_role(self, data: dict, access_token: str) -> bool:
        if has_permision(access_token) == 2 or has_permision(access_token) == 1:
            return await self.permission_from_role(
                str(data.permissions_id), str(data.role_id)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are not superuser",
            )


@lru_cache()
def get_permission_service(
    redis: RedisCache = Depends(get_redis),
    db: AsyncSession = Depends(get_session),
) -> PermissionService:

    return PermissionService(redis, db)
