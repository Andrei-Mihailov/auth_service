from os import environ as env
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv(".tests.env")


class TestSettings(BaseSettings):
    SERVICE_HOST: str = Field(default={env.get("SERVICE_HOST")})
    SERVICE_PORT: int = Field(default={env.get("SERVICE_PORT")})

    @property
    def SERVISE_URL(self):
        return f"http://{self.SERVICE_HOST}:{self.SERVICE_PORT}"


test_settings = TestSettings()
