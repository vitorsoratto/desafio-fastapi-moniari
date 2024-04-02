from fastapi import FastAPI

from config.config import settings
from api.v1.rest import init_routes
from api.v1.api import api_router as api_router_v1


def create_api():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    init_routes(app)

    return app
