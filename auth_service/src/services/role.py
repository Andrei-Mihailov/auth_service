from .base_service import BaseService
from uuid import UUID
from functools import lru_cache
from typing import Union
from fastapi import Depends, HTTPException, status

from core.constains import DEFAULT_ROLE_DATA
from models.entity import Roles
from models.user import User
from db.postgres_db import AsyncSession, get_session
from db.redis_db import RedisCache, get_redis


class RoleService(BaseService):
    def __init__(self, cache: RedisCache, storage: AsyncSession):
        super().__init__(cache, storage)
        self.model = Roles

    async def get(self, role_id: UUID) -> Union[Roles, None]:
        """Получить роль."""
        return await self.get_instance_by_id(role_id)

    async def get_by_name(self, role_name: str) -> Union[Roles, None]:
        """Получить роль по названию."""
        return await self.get_instance_by_name(role_name)

    async def create(self, role_data: dict, access_token: str) -> Roles:
        """Создание роли."""
        if await self.allow_for_change(access_token):
            return await self.create_new_instance(role_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are not superuser",
            )

    async def update(self, role_id: str, update_data: dict, access_token: str) -> Roles:
        if await self.allow_for_change(access_token):
            return await self.change_instance_data(role_id, update_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are not superuser",
            )

    async def delete(self, role_id: str, access_token: str) -> Roles:
        """Удаление роли."""
        if await self.allow_for_change(access_token):
            return await self.del_instance_by_id(role_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="you are not superuser",
            )

    async def elements(self, access_token: str):
        if await self.allow_for_change(access_token):
            return await self.get_all_instance()

    async def assign_role(self, user_id: str, role_id: str, access_token: str) -> User:
        if await self.allow_for_change(access_token, user_id):
            return await self.set_user_role(user_id, role_id)

    async def deassign_role(self, user_id: str, access_token: str) -> User:
        if await self.allow_for_change(access_token, user_id):
            return await self.del_user_role(user_id)

    async def get_default_role(self) -> Roles:
        if not (default_role := await self.get_by_name(DEFAULT_ROLE_DATA["name"])):
            default_role = await self.create(DEFAULT_ROLE_DATA)

        return default_role

    async def revoke_role(self, role: Roles, user: User, access_token: str) -> User:
        """Отзыв роли у пользователя."""
        if await self.allow_for_change(access_token, user.user_id):
            return await self.del_user_role(user, role)


@lru_cache()
def get_role_service(
    redis: RedisCache = Depends(get_redis),
    db: AsyncSession = Depends(get_session),
) -> RoleService:

    return RoleService(redis, db)
