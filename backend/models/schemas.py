from pydantic import BaseModel
from typing import List

class AssetResponse(BaseModel):
    symbol: str
    mark_price: float
    contract_value: float
    allowed_leverage: List[int]

class MarginRequest(BaseModel):
    asset: str
    order_size: float
    side: str
    leverage: int
    margin_client: float
