import logging
import logging.config as lconfig
from typing import Any

from core.config import settings

LOG_FORMAT = "%(asctime)s %(module) -10s %(funcName)-35s %(lineno) -5d: %(message)s"
LOG_DEFAULT_HANDLERS = ["console", "file"]

LOG_LEVEL = settings.logger_level


def get_logging_config(
    level: str = LOG_LEVEL,
    format: str = LOG_FORMAT,
    handlers: list[str] = LOG_DEFAULT_HANDLERS,
) -> dict[str, Any]:
    """
    Get logging config in dict format
    """

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": format},
            "default": {
                "fmt": "%(asctime)s:%(name)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "level": "ERROR",
                "formatter": "verbose",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "error.log",
                "mode": "a",
            },
        },
        "loggers": {"": {"handlers": handlers, "level": level}},
        "root": {"level": level, "formatter": "verbose", "handlers": handlers},
    }


def logger():
    lconfig.dictConfig(get_logging_config())
    logger = logging.getLogger(__file__)
    return logger


LOGGER = logger()
