from fastapi import FastAPI

from config.config import settings
from .endpoints.stock.stock_adapter import StockAdapter
from .endpoints.stock.stock_controller import StockController
from .endpoints.stock.stock_service import StockService


def init_routes(
        app: FastAPI,
):
    @app.get("/", status_code=200)
    async def check_health():
        return {"status": "ok"}

    app.include_router(
        StockController(
            stock_service=StockService(
                stock_adapter=StockAdapter()
            )
        ).router,
        prefix=f'{settings.API_V1_STR}/stock',
        tags=['API v1'],
    )
