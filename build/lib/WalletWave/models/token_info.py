from pydantic import BaseModel
from typing import List, Optional


class TokenInfo(BaseModel):
    chain: str
    address: str
    symbol: str
    name: str
    decimals: int
    logo: Optional[str] = None
    price: Optional[float] = None
    price_1h: Optional[float] = None
    price_24h: Optional[float] = None
    swaps_5m: Optional[int] = None
    swaps_1h: Optional[int] = None
    swaps_6h: Optional[int] = None
    swaps_24h: Optional[int] = None
    volume_24h: Optional[float] = None
    liquidity: Optional[float] = None
    total_supply: Optional[int] = None
    is_in_token_list: Optional[bool] = None
    hot_level: Optional[int] = None
    is_show_alert: Optional[bool] = None
    buy_tax: Optional[float] = None
    sell_tax: Optional[float] = None
    is_honeypot: Optional[bool] = None
    renounced: Optional[bool] = None
    top_10_holder_rate: Optional[float] = None
    renounced_mint: Optional[int] = None
    renounced_freeze_account: Optional[int] = None
    burn_ratio: Optional[str] = None
    burn_status: Optional[str] = None


class TokenInfoResponse(BaseModel):
    code: int
    msg: str
    data: List[TokenInfo]
