import os
from logging import config as logging_config

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

class AuthJWT(BaseModel):
    secret_key: str = "secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 20
    refresh_token_expire_minutes: int = 30 * 24 * 60 # 30 дней

class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    # project_name: str

    # # Настройки postgres
    # db_name: str
    # db_user: str
    # db_password: str
    # db_host: str
    # db_port: int

    # # Настройки Redis
    # redis_host: str
    # redis_port: int
    auth_jwt: AuthJWT = AuthJWT()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    class Config:
        env_file = ".env"


settings = Settings()

page_max_size = 100
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PostgreSQLConfig(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int


# pg_config_data = PostgreSQLConfig(
#     dbname=settings.db_name,
#     user=settings.db_user,
#     password=settings.db_password,
#     host=settings.db_host,
#     port=settings.db_port
# )
