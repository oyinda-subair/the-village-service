import logging
import sys
from loguru import logger
from app.core.settings import Settings
from app.core.logging import InterceptHandler


"""Custom logging"""


def setup_app_logging(*, config: Settings) -> None:
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    )
