import multiprocessing
import gunicorn.app.base
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from contextlib import asynccontextmanager

from api.v1 import users, roles, access_users
from db import postgres_db
from db import redis_db
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_db.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    # await postgres_db.purge_database()

    await postgres_db.create_database()
    yield
    await redis_db.redis.close()


app = FastAPI(
    lifespan=lifespan,
    title="Сервис авторизации",
    description="Реализует методы идентификации, аутентификации, авторизации",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


app.include_router(users.router, prefix="/api/v1/users")
app.include_router(roles.router, prefix="/api/v1/roles")
app.include_router(access_users.router, prefix="/api/v1/access_users")


if __name__ == "__main__":
    options = {
        "bind": "%s:%s" % ("0.0.0.0", "8000"),
        "workers": number_of_workers(),
        "worker_class": "uvicorn.workers.UvicornWorker",
    }

    StandaloneApplication(app, options).run()
