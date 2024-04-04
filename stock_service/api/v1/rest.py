from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config.config import settings
from exceptions.default_exception import DefaultException
from .endpoints.stock.stock_controller import StockController


def init_routes(
        app: FastAPI,
):
    @app.get("/", status_code=200)
    async def check_health():
        return {"status": "ok"}

    app.include_router(
        StockController().router,
        prefix=f'{settings.API_V1_STR}/stock',
        tags=['API v1'],
    )

    @app.exception_handler(DefaultException)
    async def default_exception_handler(request: Request, error: DefaultException):
        return JSONResponse(error.to_dict(), status_code=error.code)
