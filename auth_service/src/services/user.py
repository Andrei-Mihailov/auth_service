from fastapi import Depends, HTTPException, status
from functools import lru_cache
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession


from models.entity import User
from .base_service import BaseService
from models.auth import Authentication, Tokens
from .utils import (
    create_refresh_token,
    create_access_token,
    decode_jwt,
    validate_password,
    hash_password,
    check_date_and_type_token,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from core.config import settings
from db.postgres_db import get_session
from db.redis_db import RedisCache, get_redis


class UserService(BaseService):
    def __init__(self, cache: RedisCache, storage: AsyncSession):
        super().__init__(cache, storage)
        self.model = User

    def token_decode(self, token):
        return decode_jwt(jwt_token=token)

    async def get_validate_user(self, user_login: str, user_password: str) -> User:
        user: User = await self.get_user_by_login(user_login)
        if user is None:  # если в бд не нашли такой логин
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid login"
            )
        if not user.check_password(user_password):  # если пароль не совпадает
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="uncorrect password"
            )
        if not user.active:  # если пользователь неактивен
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user is deactive"
            )

        return user

    async def change_user_info(
        self,
        access_token: str,
        user_data: dict
    ) -> bool:
        payload = self.token_decode(access_token)
        user_uuid = payload.get("sub")

        if check_date_and_type_token(payload, ACCESS_TOKEN_TYPE):
            # проверка access токена в блэк листе redis
            if not await self.get_from_black_list(access_token):
                user = await self.change_instance_data(user_uuid, user_data)
                if user is None:  # если в бд пг не нашли такой uuid
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found"
                    )
            else:
                return False  # TODO: проверить варианты ответа пользователю
        return True

    async def create_user(
        self,
        user_params
    ) -> bool:
        res = await self.create_new_instance(user_params)
        return True if res else False

    async def login(self, user_login: str, user_password: str) -> Tokens:
        user = await self.get_validate_user(user_login, user_password)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        # добавление refresh токена в вайт-лист редиса
        await self.add_to_white_list(refresh_token, 'refresh')
        return Tokens(access_token=access_token, refresh_token=refresh_token), user

    async def refresh_access_token(
            self,
            access_token: str,
            refresh_token: str
    ) -> Tokens:
        # Декодирование refresh-токена
        payload = self.token_service.decode_jwt(refresh_token)
        user_uuid = payload.get("sub")

        # Проверка типа и срока действия токена
        if self.token_service.check_date_and_type_token(payload, REFRESH_TOKEN_TYPE):
            # Проверка наличия refresh-токена в списке разрешенных
            if await self.token_service.get_from_white_list(refresh_token):
                # Получение пользователя по UUID
                user = await self.user_service.get_instance_by_id(user_uuid)

                # Генерация новых токенов
                new_access_token = self.token_service.create_access_token(user)
                new_refresh_token = self.token_service.create_refresh_token(user)

                # Добавление старого access-токена в черный список
                await self.token_service.add_to_black_list(access_token, 'access')

                # Удаление старого refresh-токена из списка разрешенных
                await self.token_service.del_from_white_list(refresh_token)

                # Добавление нового refresh-токена в список разрешенных
                await self.token_service.add_to_white_list(new_refresh_token, 'refresh')

                # Возврат новых токенов
                return Tokens(access_token=new_access_token, refresh_token=new_refresh_token)
            else:
                # Если refresh-токен не найден в списке разрешенных, выбросить исключение
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh-токен недействителен или истек срок его действия"
                )
        else:
            # Обработка ситуации, когда refresh-токен недействителен или истек срок его действия
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh-токен недействителен или истек срок его действия"
            )


@ lru_cache()
def get_user_service(
        redis: RedisCache = Depends(get_redis),
        db: AsyncSession = Depends(get_session),


) -> UserService:

    return UserService(redis, db)
