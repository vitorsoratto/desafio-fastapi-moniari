from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Request, Query

from autentication.autentication import authenticate
from config.config import settings
from exceptions.default_exception import DefaultException
from schemas.user_stock.user_stock_schema import UserStockSchema


class UserController:
    """
    Controller
    """

    def __init__(self):
        self.router = APIRouter()

        @self.router.get(
            '',
            response_model=UserStockSchema,
        )
        async def get_stock(
                request: Request, user: dict = Depends(authenticate), q: str | None = None
        ) -> UserStockSchema:
            stock_symbol = q
            request.app.logger.info(f'User: "{user.get('username')}" - Stock: "{stock_symbol.upper()}"')
            response_json = {}

            try:
                async with ClientSession() as session:
                    async with session.get(
                            f'{settings.STOCK_API_URL}/api/v1/stock/{stock_symbol}'
                    ) as response:
                        content_type = response.headers.get('Content-Type')

                        if 'application/json' not in content_type:
                            raise DefaultException(message='Error finding the stock', code=400)
                        elif response.status == 404:
                            raise DefaultException(message='Not Found', code=404)
                        else:
                            response_json = await response.json()

                            user_stock = UserStockSchema.parse(response_json)
                            request.app.logger.info(f'response - {response_json}')
                            return user_stock

            except DefaultException as ex:
                request.app.logger.error(
                    f'Stock: "{stock_symbol.upper()}"'
                    f' / {response_json=} / {ex=}'
                )
                raise
