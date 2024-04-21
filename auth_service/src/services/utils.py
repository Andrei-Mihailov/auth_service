import jwt
import uuid

from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status

from core.config import settings
from models.user import User

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(token_type: str, token_data: dict, expire_minutes: int) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)

    now_utc = datetime.now(timezone.utc)
    now_unix = now_utc.timestamp()
    expire_utc = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    expire_unix = expire_utc.timestamp()

    jwt_payload.update(exp=expire_unix, iat=now_unix)
    return encode_jwt(jwt_payload)


def create_access_token(user: User):
    # TODO: добавить разрешения или роль для пользователей в тело ключа
    # добавлен uuid токена
    payload = {
        "sub": str(user.id),  # userid
        "role": "user",  # определиться с тем, храним ли тут роли, одна ли роль или несколько
        "self_uuid": str(uuid.uuid4()),
    }
    return create_jwt(
        ACCESS_TOKEN_TYPE, payload, settings.auth_jwt.access_token_expire_minutes
    )


def create_refresh_token(user: User):
    payload = {"sub": str(user.id), "self_uuid": str(uuid.uuid4())}
    return create_jwt(
        REFRESH_TOKEN_TYPE, payload, settings.auth_jwt.refresh_token_expire_minutes
    )


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.secret_key,
    algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.encode(payload, private_key, algorithm)


def decode_jwt(
    jwt_token: str,
    private_key: str = settings.auth_jwt.secret_key,
    algorithm: str = settings.auth_jwt.algorithm,
):
    try:
        decoded = jwt.decode(jwt_token, private_key, algorithms=[algorithm])
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    except jwt.exceptions.InvalidAlgorithmError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token algorithm"
        )
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature"
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired, refresh token"
        )
    return decoded


def hash_password(
    password: str,
) -> bytes:
    hash_pass = settings.pwd_context.hash(password)
    return hash_pass


def validate_password(hashed_password: bytes, password: str) -> bool:
    try:
        return settings.pwd_context.verify(password, hashed_password)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password"
        )


def check_date_and_type_token(payload: dict, type_token_need: str) -> bool:

    type_token = payload.get("type")
    # проверка типа токена
    if type_token != type_token_need:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type"
        )
    # проверяем срок действия access токена
    exp = payload.get("exp")
    now = datetime.timestamp(datetime.now())
    if now > exp:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired, refresh token"

        )
    return True
