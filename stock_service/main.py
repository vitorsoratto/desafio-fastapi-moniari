import logging
from pathlib import Path

from fastapi import FastAPI
from config.config import settings
from api.v1.rest import init_routes
from utils.custom_logging import setup_logging


def create_api():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )
    logger = setup_logging()
    app.logger = logger

    init_routes(app)

    return app
