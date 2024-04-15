from datetime import timedelta, datetime, timezone

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from core.config import settings
from models.user import User

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(token_type: str,
               token_data: dict,
               expire_minutes: int) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)

    now_utc = datetime.now(timezone.utc)
    now_unix = now_utc.timestamp()
    expire_utc = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    expire_unix = expire_utc.timestamp()

    jwt_payload.update(
        exp=expire_unix,
        iat=now_unix
    )
    return encode_jwt(jwt_payload)


def create_access_token(user: User):
    # TODO: добавить разрешения или роль для пользователей в тело ключа
    # TODO: возможно добавить uuid токена
    payload = {
            "sub": user.user_id, #userid
            "role": "user" #определиться с тем, храним ли тут роли, одна ли роль или несколько
    }
    return create_jwt(ACCESS_TOKEN_TYPE,
                      payload,
                      settings.auth_jwt.access_token_expire_minutes)


def create_refresh_token(user: User):
    payload = {
            "sub": user.user_id,
    }
    return create_jwt(REFRESH_TOKEN_TYPE,
                      payload,
                      settings.auth_jwt.refresh_token_expire_minutes)


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.secret_key,
        algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.encode(payload, private_key, algorithm)



def decode_jwt(
        jwt_token: str,
        private_key: str = settings.auth_jwt.secret_key,
        algorithm: str = settings.auth_jwt.algorithm
):
    try:
        decoded = jwt.decode(jwt_token,
                         private_key,
                         algorithms=[algorithm])
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
    return decoded


def hash_password(
        password: str,        
) -> bytes:
    hash_pass = settings.pwd_context.hash(password)
    return hash_pass


def validate_password(
       hashed_password: bytes, 
       password: str
) -> bool:
    return settings.pwd_context.verify(password, hashed_password)

    