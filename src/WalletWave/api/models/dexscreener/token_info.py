from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Optional, Any


class Token(BaseModel):
    address: str
    name: str
    symbol: str


class TxnData(BaseModel):
    buys: Optional[int] = 0
    sells: Optional[int] = 0


class Liquidity(BaseModel):
    usd: float
    base: float
    quote: float


class Website(BaseModel):
    url: HttpUrl


class Social(BaseModel):
    platform: Optional[str] = "Unknown"
    handle: Optional[str] = "Unknown"


class Info(BaseModel):
    imageUrl: Optional[HttpUrl] = None
    websites: List[Website] = Field(default_factory=list)
    socials: List[Social] = Field(default_factory=list)


class DexPair(BaseModel):
    chainId: str
    dexId: str
    url: HttpUrl
    pairAddress: str = Field(..., min_length=11, max_length=45)
    labels: List[str] = Field(default_factory=list)
    baseToken: Token
    quoteToken: Token
    priceNative: str
    priceUsd: str
    txns: Dict[str, TxnData] = Field(default_factory=dict)
    volume: Dict[str, float] = Field(default_factory=dict)
    priceChange: Dict[str, float] = Field(default_factory=dict)
    liquidity: Liquidity
    fdv: float
    marketCap: float
    pairCreatedAt: int
    info: Optional[Info] = None
    boosts: Dict[str, Any] = Field(default_factory=dict)


class DexscreenerPairResponse(BaseModel):
    data: List[DexPair]
