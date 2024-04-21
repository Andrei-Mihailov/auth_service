""" from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST:str
    DB_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    SERVICE_HOST: str
    SERVICE_PORT: int

    @property
    def SERVISE_URL(self):
        return f"http://{self.SERVICE_HOST}:{self.SERVICE_PORT}"

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

test_settings = TestSettings() """
