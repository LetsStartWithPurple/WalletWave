from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class TagRank(BaseModel):
    fresh_wallet: Optional[int] = None


class DailyProfit(BaseModel):
    timestamp: int
    profit: float


class RankEntry(BaseModel):
    wallet_address: str
    address: str
    realized_profit: float
    buy: int
    sell: int
    last_active: int
    realized_profit_1d: Optional[float] = None
    realized_profit_7d: Optional[float] = None
    realized_profit_30d: Optional[float] = None
    pnl_30d: Optional[float] = None
    pnl_7d: Optional[float] = None
    pnl_1d: Optional[float] = None
    txs_30d: Optional[int] = None
    buy_30d: Optional[int] = None
    sell_30d: Optional[int] = None
    balance: Optional[float] = None
    eth_balance: Optional[float] = None
    sol_balance: Optional[float] = None
    trx_balance: Optional[float] = None
    twitter_username: Optional[str] = None
    avatar: Optional[str] = None
    ens: Optional[str] = None
    tag: Optional[str] = None
    tag_rank: Optional[TagRank] = None
    nickname: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    twitter_name: Optional[str] = None
    followers_count: Optional[int] = 0
    is_blue_verified: Optional[int] = 0
    twitter_description: Optional[str] = None
    name: Optional[str] = None
    avg_hold_time: Optional[int] = 0
    recent_buy_tokens: List = Field(default_factory=list)
    winrate_7d: Optional[float] = None
    avg_cost_7d: Optional[float] = None
    pnl_lt_minus_dot5_num_7d: Optional[int] = None
    pnl_minus_dot5_0x_num_7d: Optional[int] = None
    pnl_lt_2x_num_7d: Optional[int] = None
    pnl_2x_5x_num_7d: Optional[int] = None
    pnl_gt_5x_num_7d: Optional[int] = None
    pnl_lt_minus_dot5_num_7d_ratio: Optional[float] = None
    pnl_minus_dot5_0x_num_7d_ratio: Optional[float] = None
    pnl_lt_2x_num_7d_ratio: Optional[float] = None
    pnl_2x_5x_num_7d_ratio: Optional[float] = None
    pnl_gt_5x_num_7d_ratio: Optional[float] = None
    daily_profit_7d: List[DailyProfit] = Field(default_factory=list)
    txs: Optional[int] = None
    token_num_7d: Optional[int] = None
    avg_holding_period_7d: Optional[float] = None


class WalletsResponse(BaseModel):
    code: int
    msg: str
    data: Dict[str, List[RankEntry]]

    @property
    def rank(self) -> List[RankEntry]:
        """
        Getter for the 'rank' data

        Returns:
            List[RankEntry]: A list of RankEntry objects or an empty list if 'rank' is missing.
        """

        return self.data.get("rank", [])