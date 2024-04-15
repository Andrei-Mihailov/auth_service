from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.user import User
from db.postgres_db import postgres
from db.redis_db import RedisCache, get_redis
from models.user import User
from .base_service import BaseService
from models.auth import Authentication, Tokens
from .utils import (create_refresh_token,
                    create_access_token,
                    decode_jwt,
                    validate_password,
                    hash_password,
                    ACCESS_TOKEN_TYPE
)
from ..core.config import settings

class UserService(BaseService):
    async def get_validate_user(self, user_login: str, user_password: str) -> User:
        # TODO: получить пользователя по логину и паролю в pg (модель User) 
        #res = await postgres.execute_query("")
        user = User()
        if user == None: #если в бд не нашли такой логин
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='invalid username'
            )
        if not validate_password(password=user_password,
                             hashed_password=user.password
        ): # если пароль не совпадает
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='uncorrect password'
            )
        if not user.active: # если пользователь неактивен
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='user is deactive'
            )
        
        return user
    

    async def get_current_user(token: str = Depends(settings.oauth2_scheme)):
        payload = decode_jwt(token)
        user_uuid = payload.get("sub")
        type_token = payload.get("type")
        #получение доступа только по access токену
        if type_token != ACCESS_TOKEN_TYPE:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='invalid token type'
            )
        #проверяем срок действия access токена
        exp = payload.get("exp")
        now = datetime.timestamp(datetime.now())
        if now > exp:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='token expire'
            )
        # TODO: получить пользователя по uuid в pg (модель User)
        #res = await postgres.execute_query("") #поиск по uuid из бд через зпрос или через sqlAlchemy?
        user = User()
        if user == None: #если в бд пг не нашли такой uuid
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='user not found'
            )
        return user
    

    async def change_user_info(id_user, 
                               firstname: str | None,
                               lastname: str | None,
                               login: str | None,
                               password: str | None,
                               user: User = Depends(get_current_user)
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
        #await postgres.save_user()
        return True


    async def create_user(firstname: str | None,
                          lastname: str | None,
                          login: str,
                          password: str
    ) -> bool:
        user = User()
        if firstname:
            user.first_name = firstname
        if lastname:
            user.last_name = lastname
        if login:
            user.login = login
        if password:
            user.password = hash_password(password)
        
        # TODO: создание нового пользователя в бд пг
        #await postgres.save_user()
        return True
      
    
    async def login(self, user_login: str, user_password: str) -> Tokens:
        user = await self.get_validate_user(user_login, user_password)    
                
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        return Tokens(access_token, refresh_token)
