from .base_service import BaseService
from uuid import UUID
from functools import lru_cache
from typing import Union
from fastapi import Depends

from sqlalchemy import select

# from core.constants import DEFAULT_ROLE_DATA
from models.roles import Role
from models.user import User
from db.postgres_db import AsyncSession, get_session
from db.redis_db import RedisCache, get_redis


class RoleService(BaseService):
    def __init__(self, cache: RedisCache, storage: AsyncSession):
        super().__init__(cache, storage)

    async def get(self, session: AsyncSession, role_id: UUID) -> Union[Role, None]:
        """Получить роль."""
        return await self.get_instance_by_id(role_id)

    async def get_by_name(self, session: AsyncSession,
                          role_name: str) -> Union[Role, None]:
        """Получить роль по названию."""
        return await self.get_instance_by_name(role_name)

    async def create(self, session: AsyncSession, role_data: dict) -> Role:
        """Создание роли."""
        return await self.create_new_instance(role_data)

    async def update(
        self, session: AsyncSession, role: Role, update_data: dict
    ) -> Role:
        await self.change_instance_data(role.id, update_data)

    async def delete(self, session: AsyncSession, role: Role) -> Role:
        """Удаление роли."""
        await self.del_instance_by_id(role.id)

        return role

    async def elements(self, session: AsyncSession):
        return await self.get_all_instance()

    async def assign_role(self, session: AsyncSession, role: Role, user: User) -> User:
        return await self.set_user_role(user, role)

    async def get_default_role(self, session: AsyncSession) -> Role:
        if not (
            default_role := await self.get_by_name(session, DEFAULT_ROLE_DATA["name"])
        ):
            default_role = await self.create(session, DEFAULT_ROLE_DATA)

        return default_role


@lru_cache()
def get_role_service(
        redis: RedisCache = Depends(get_redis),
        db: AsyncSession = Depends(get_session),
) -> RoleService:

    return RoleService(redis, db)
