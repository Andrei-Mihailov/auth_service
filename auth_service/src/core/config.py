import os
from logging import config as logging_config
from pydantic import BaseModel
from pydantic_settings import BaseSettings


from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


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
