import logging
from gunicorn.app.base import BaseApplication
from ce_portal.asgi import application
from loguru import logger


LOG_LEVEL = logging.getLevelName("DEBUG")
JSON_LOGS = False
WORKERS = 3


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, f"{record.getMessage()}"
        )


class StandaloneApplication(BaseApplication):

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


if __name__ == "__main__":
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logging.getLogger('asyncio').setLevel(logging.ERROR)

    options = {
        "bind": "0.0.0.0:8777",
        "workers": WORKERS,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "daemon": True,
    }

    StandaloneApplication(application, options).run()
