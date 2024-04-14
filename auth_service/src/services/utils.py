from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.secret_key,
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
):
    to_encode = payload.copy()
    now = datetime.timestamp(datetime.now())
    expire = datetime.timestamp(datetime.now() + timedelta(minutes=expire_minutes))
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(payload, private_key, algorithm)
    return encoded


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

    