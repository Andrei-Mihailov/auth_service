import multiprocessing
import gunicorn.app.base
import click
import asyncio
import functools as ft
import sys

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from contextlib import asynccontextmanager

from api.v1 import users, roles, permissions
from db import postgres_db
from db import redis_db
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_db.redis = Redis(host=settings.redis_host, port=settings.redis_port)
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
app.include_router(permissions.router, prefix="/api/v1/permissions")


def async_cmd(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "--username",
    default="test",
    prompt="Enter username",
    help="Username for the superuser",
)
@click.option(
    "--password",
    default="test",
    prompt="Enter password",
    help="Password for the superuser",
)
@async_cmd
async def create_superuser(username, password):
    from models.entity import User
    from sqlalchemy.future import select

    await postgres_db.create_database()
    async with postgres_db.async_session() as session:
        result = await session.execute(select(User).filter(User.login == username))
        existing_user = result.scalars().first()
        if existing_user:
            click.echo("User with this login already exists!")
            return

        # Создаем суперпользователя
        superuser_data = {"login": username, "password": password, "is_superuser": True}
        instance = User(**superuser_data)
        session.add(instance)
        try:
            await session.commit()
        except Exception as e:
            print(f"Ошибка при создании объекта: {e}")
            return None

        click.echo(f"Superuser {username} created successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        create_superuser()
    else:
        options = {
            "bind": "%s:%s" % ("0.0.0.0", "8000"),
            "workers": number_of_workers(),
            "worker_class": "uvicorn.workers.UvicornWorker",
        }

        StandaloneApplication(app, options).run()
