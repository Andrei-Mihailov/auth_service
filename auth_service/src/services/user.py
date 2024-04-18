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
from db.postgres_db import PostgresDatabase, get_session
from db.redis_db import RedisCache, get_redis


class UserService(BaseService):
    def __init__(self, cache: RedisCache, storage: AsyncSession):
        super().__init__(cache, storage)

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

    async def get_current_user(self, token: str = Depends(settings.oauth2_scheme)):
        payload = decode_jwt(token)
        user_uuid = payload.get("sub")

        if check_date_and_type_token(payload, ACCESS_TOKEN_TYPE):
            # TODO: проверка access токена в блэк листе redis

            # TODO: получить пользователя по uuid в pg (модель User)
            # res = await postgres.execute_query("") #поиск по uuid из бд через зпрос или через sqlAlchemy?
            user = User()
            if user is None:  # если в бд пг не нашли такой uuid
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found"
                )
            return user

    async def change_user_info(
        self,
        id_user,
        firstname: Union[str, None],
        lastname: Union[str, None],
        login: Union[str, None],
        password: Union[str, None],
        user: User = Depends(get_current_user),
    ) -> bool:
        if firstname:
            user.first_name = firstname
        if lastname:
            user.last_name = lastname
        if login:
            user.login = login
        if password:
            user.password = hash_password(password)

        # TODO: сохранение изменений пользователя в бд пг
        # await postgres.save_user()
        return True

    async def create_user(
        self,
        user_params: dict
    ) -> bool:
        res = await self.create_new_user(user_params)
        return res

    async def login(self, user_login: str, user_password: str) -> Tokens:
        user = await self.get_validate_user(user_login, user_password)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        # TODO: добавление refresh токена в вайт-лист редиса
        # TODO: добавление в бд pg данных об аутентификации модель Authentication

        return Tokens(access_token, refresh_token)

    async def refresh_access_token(
        self,
        access_token: str,
        refresh_token: str
    ) -> Tokens:

        payload = decode_jwt(refresh_token)
        user_uuid = payload.get("sub")

        if check_date_and_type_token(payload, REFRESH_TOKEN_TYPE):
            # TODO: проверка наличия refresh токена в бд redis (хорошо, если он там есть)

            # TODO: наити пользователя по user_uuid, вернуть (модель User)
            user = User()
            new_access_token = create_access_token(user)
            new_refresh_token = create_refresh_token(user)
            # TODO: добавить старый access токен в блэк-лист redis
            # TODO: удалить старый refresh токен из вайт-листа redis
            # TODO: добавить новый refresh токен в вайт-лист redis
            return Tokens(new_access_token, new_refresh_token)

    async def login_history(
        id_user_history: str,
        access_token: str
    ) -> list[Authentication]:

        payload = decode_jwt(access_token)
        user_uuid = payload.get("sub")

        if check_date_and_type_token(payload, ACCESS_TOKEN_TYPE):
            # TODO: проверка наличия access токена в блэк-листе бд redis (плохо, если он там есть)
            # TODO: найти пользователя по user_uuid, проверяем есть ли пользователь от лица которого выполняется действие
            # TODO: получить историю авторизаций по id_user_history модель Authentication

            return list[Authentication]


@lru_cache()
def get_user_service(
        redis: RedisCache = Depends(get_redis),
        db: AsyncSession = Depends(get_session),
) -> UserService:

    return UserService(redis, db)
