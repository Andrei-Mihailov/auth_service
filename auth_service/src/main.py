import multiprocessing

import gunicorn.app.base
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="Сервис авторизации",
    description="Реализует методы аутентификации, авторизации",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
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


# app.include_router()


if __name__ == "__main__":
    options = {
        "bind": "%s:%s" % ("0.0.0.0", "8000"),
        "workers": number_of_workers(),
        "worker_class": "uvicorn.workers.UvicornWorker",
    }

    StandaloneApplication(app, options).run()
