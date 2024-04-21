from fastapi import Depends, HTTPException, status
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from models.entity import Authentication
from .base_service import BaseService
from .utils import (
    decode_jwt,
    check_date_and_type_token,
    ACCESS_TOKEN_TYPE
)
from db.postgres_db import get_session
from db.redis_db import RedisCache, get_redis


class AuthService(BaseService):
    def __init__(self, cache: RedisCache, storage: AsyncSession):
        super().__init__(cache, storage)
        self.model = Authentication

    async def new_auth(self, auth_params) -> None:
        # добавление в бд pg данных об аутентификации модель Authentication
        await self.create_new_instance(auth_params)

    async def login_history(
        self,
        user_id: str,
        access_token: str
    ) -> list[Authentication]:
        payload = decode_jwt(jwt_token=access_token)
        user_uuid = payload.get("sub")
        # TODO: проверить разрешение для просмотра истории входа
        if check_date_and_type_token(payload, ACCESS_TOKEN_TYPE):
            # проверка наличия access токена в блэк-листе бд redis (плохо, если он там есть)
            if not await self.get_from_black_list(access_token):
                # получить историю авторизаций по id_user_history модель Authentication
                auths_list = await self.get_login_history(user_id)
                if auths_list is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
                    )
                return auths_list
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="uncorrect token"
                )


@lru_cache()
def get_auth_service(
        redis: RedisCache = Depends(get_redis),
        db: AsyncSession = Depends(get_session),
) -> AuthService:

    return AuthService(redis, db)
