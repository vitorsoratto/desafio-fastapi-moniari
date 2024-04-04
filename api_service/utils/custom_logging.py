import json
import logging
import sys
from pathlib import Path
from pprint import pformat
from typing import Any

from loguru import logger
from fastapi import Request


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


def get_config():
    config_path = Path('..').with_name("logger_config.json")
    config = None
    with open(config_path) as config_file:
        config = json.load(config_file)

    log = config.get('logger')
    return log


def setup_logging():
    log = get_config()
    path = log.get('path')
    logger_format = log.get('format')

    logger.remove()

    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=True,
        level='INFO',
        format=logger_format,
    )
    logger.add(
        str(path),
        enqueue=True,
        backtrace=True,
        level='INFO',
        format=logger_format,
    )

    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    logging.getLogger().handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    return logger

