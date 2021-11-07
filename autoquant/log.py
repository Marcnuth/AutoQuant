import logging
from logging.config import dictConfig


dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "[%(asctime)s] [%(process)d:%(thread)d] [%(levelname)s] [%(name)s] %(filename)s:%(funcName)s:%(lineno)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "basic",
            "stream": "ext://sys.stdout"
        },
    },
    "loggers": {
        "autoquant": {
            "handlers": ["console"],
            "propagate": "true",
            "level": "DEBUG"
        }
    }
})

logger = logging.getLogger(__name__)
logger.debug('AutoQuant logs will be printed in console')
