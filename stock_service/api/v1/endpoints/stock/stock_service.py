from schemas.stock.stock_schema import StockSchema


class StockService:
    def __init__(self, stock_adapter):
        self.adapter = stock_adapter

    async def get_stock(self, stock_symbol: str) -> StockSchema:
        stock = await self.adapter.get_stock(stock_symbol=stock_symbol)
        return StockSchema(**stock.dict())
