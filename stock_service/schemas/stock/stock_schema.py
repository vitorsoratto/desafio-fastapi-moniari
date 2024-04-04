from pydantic import BaseModel
from typing import Optional


class StockSchema(BaseModel):
    symbol: Optional[str] | None
    name: Optional[str] | None
    date: Optional[str] = None
    time: Optional[str] = None
    open: Optional[float] = None
    low: Optional[float] = None
    high: Optional[float] = None
    close: Optional[float] = None
