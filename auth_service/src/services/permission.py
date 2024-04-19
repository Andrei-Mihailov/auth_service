from models.user import User
from models.permission import Permission
from models.role import Role
from base_service import BaseService
from utils import decode_jwt, check_date_and_type_token, ACCESS_TOKEN_TYPE
from fastapi import HTTPException, status
from typing import List
from functools import lru_cache
from db.redis_db import RedisCache, get_redis
from db.postgres_db import AsyncSession, get_session
from fastapi import Depends

class PermissionService(BaseService):
    async def get_user_permissions(self, access_token: str) -> List[Permission]:
        payload = decode_jwt(access_token)
        user_uuid = payload.get("sub")

        if check_date_and_type_token(payload, ACCESS_TOKEN_TYPE):
            # TODO: Получить пользователя из базы данных, используя user_uuid
            user = User()

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Пользователь не найден"
                )

            roles = user.roles

            permissions = []
            for role in roles:
                permissions.extend(role.permissions)

            return permissions

    async def has_permission(self, access_token: str, permission_name: str) -> bool:
        permissions = await self.get_user_permissions(access_token)

        for permission in permissions:
            if permission.name == permission_name:
                return True

        return False

    async def create_permission(self, name: str) -> Permission:
        # TODO: Реализовать создание нового разрешения в базе данных
        permission = Permission(name=name)
        return permission

    async def assign_permission_to_role(self, role_name: str, permission_name: str) -> bool:
        # TODO: Реализовать назначение разрешения роли в базе данных.
        role = Role(name=role_name)

        permission = Permission(name=permission_name)

        role.permissions.append(permission)
        return True

    async def remove_permission_from_role(self, role_name: str, permission_name: str) -> bool:
        # TODO: Реализовать удаление разрешения из роли в базе данных.
        role = Role(name=role_name)

        permission = Permission(name=permission_name)

        role.permissions.remove(permission)
        return True

@lru_cache()
def get_permission_service(
        redis: RedisCache = Depends(get_redis),
        db: AsyncSession = Depends(get_session),
) -> PermissionService:

    return PermissionService(redis, db)