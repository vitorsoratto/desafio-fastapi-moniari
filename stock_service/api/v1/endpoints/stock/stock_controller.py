from fastapi import APIRouter, Request
from config.config import settings
from exceptions.default_exception import DefaultException
from schemas.stock.stock_schema import StockSchema
from aiohttp import ClientSession

from utils.utils import csv_to_json


class StockController:
    """
    Controller for getting stock data
    """
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route(
            '/{stock_symbol}',
            self.get_stock,
            methods=['GET'],
            response_model=StockSchema,
        )

    async def get_stock(self, stock_symbol: str, request: Request) -> StockSchema:
        """
        Get stock data from API
        :param stock_symbol: Ex: TEAM.US, JJSF.US
        :param request
        :return:
        """
        request.app.logger.info(f'Stock: "{stock_symbol.upper()}"')
        response_json = {}
        try:
            async with ClientSession() as session:
                async with session.get(
                        f'{settings.API_STOCK_URL}?s={stock_symbol}{settings.API_STOCK_SUFFIX}&e=csv'
                ) as response:
                    content_type = response.headers.get('Content-Type')

                    if 'text/csv' not in content_type:
                        raise DefaultException
                    else:
                        csv_response = await response.text()
                        response_json = csv_to_json(csv_response)

                        if response_json.get('date') == 'N/D':
                            raise DefaultException

                        request.app.logger.info(f'response - {response_json}')
                        return StockSchema(**response_json)

        except DefaultException as ex:
            message = response.reason if not ex.message else 'Not Found'
            code = response.status if not ex.code else response.status

        request.app.logger.error(
            f'Stock: "{stock_symbol.upper()}"'
            f' / {message=} / {code=} / {response_json=}'
        )

        raise DefaultException(detail=f"Stock '{stock_symbol.upper()}'", message=message, code=code)
