import pybase64
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15


from models.user import User
from db.postgres_db import postgres
from db.redis_db import RedisCache, get_redis
from models.user import User
from .base_service import BaseService


class UserService(BaseService):
    # Секретный ключ для создания и проверки JWT-токенов
    SECRET_KEY = "secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Функция для генерации JWT-токена
    def create_access_token(self, data: dict, private_key_path: str, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

# Функция для проверки JWT-токена и получения текущего пользователя


async def get_current_user(token: str = Depends(UserService.oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, UserService.SECRET_KEY, algorithms=[UserService.ALGORITHM])
        user_id = decoded_token.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        # Здесь логику получения пользователя по user_id
        user = User(...)

        return user

    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    except jwt.exceptions.InvalidAlgorithmError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token algorithm"
        )
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature"
        )
