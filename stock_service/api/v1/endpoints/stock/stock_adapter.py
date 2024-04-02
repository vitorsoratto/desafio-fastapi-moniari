from config.config import settings
from exceptions.default_exception import DefaultException
from schemas.stock.stock_schema import StockSchema
from aiohttp import ClientSession
import csv, io, json

from utils import csv_to_json


class StockAdapter:

    async def get_stock(self, stock_symbol: str) -> StockSchema:
        response_json = {}
        try:
            async with ClientSession() as session:
                async with session.get(
                        f'{settings.API_STOCK_URL}?s={stock_symbol}{settings.API_STOCK_SUFFIX}&e=csv'
                ) as response:
                    if response.headers.get('Content-Type').find('text/csv') >= 0:
                        csv_response = await response.text()
                        response_json = csv_to_json(csv_response)

                    if response.status != 200:
                        raise DefaultException

            return StockSchema(**response_json)

        except DefaultException as ex:
            message = response.reason if not ex.message else response.reason
            code = response.status if not ex.code else response.status

            raise DefaultException(detail=f"Stock '{stock_symbol}'", message=message, code=code)
