from pydantic import BaseModel
from typing import Optional


class UserStockSchema(BaseModel):
    simbolo: Optional[str] | None
    nome_da_empresa: Optional[str] | None
    cotacao: Optional[float] = None

    @classmethod
    def parse(cls, response: dict):
        return cls(
            simbolo=response.get('symbol'),
            nome_da_empresa=response.get('name'),
            cotacao=response.get('close')
        )
