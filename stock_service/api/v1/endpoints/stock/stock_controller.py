from fastapi import APIRouter

from schemas.stock.stock_schema import StockSchema


class StockController:
    def __init__(self, stock_service):
        self.service = stock_service
        self.router = APIRouter()

        self.router.add_api_route(
            '/{stock_symbol}',
            self.get_stock,
            methods=['GET'],
            response_model=StockSchema,
        )

    async def get_stock(self, stock_symbol: str) -> StockSchema:
        stock = await self.service.get_stock(stock_symbol=stock_symbol)

        return stock

