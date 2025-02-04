from pydantic import BaseModel, Field
from typing import List, Optional


class TagRank(BaseModel):
    fresh_wallet: Optional[int] = None


class Risk(BaseModel):
    token_active: Optional[str] = None
    token_honeypot: Optional[str] = None
    token_honeypot_ratio: Optional[float] = None
    no_buy_hold: Optional[str] = None
    no_buy_hold_ratio: Optional[float] = None
    sell_pass_buy: Optional[str] = None
    sell_pass_buy_ratio: Optional[float] = None
    fast_tx: Optional[str] = None
    fast_tx_ratio: Optional[float] = None


class WalletInfo(BaseModel):
    twitter_bind: bool
    twitter_fans_num: int
    eth_balance: str
    sol_balance: str
    trx_balance: str
    balance: str
    total_value: float
    unrealized_profit: float
    unrealized_pnl: float
    realized_profit: float
    pnl: float
    pnl_7d: float
    pnl_30d: float
    realized_profit_7d: float
    realized_profit_30d: float
    all_pnl: float
    total_profit: float
    total_profit_pnl: float
    buy_30d: int
    sell_30d: int
    buy_7d: int
    sell_7d: int
    buy: int
    sell: int
    last_active_timestamp: int
    followers_count: int
    is_contract: bool
    updated_at: int
    
    # Fields with default values
    token_num: Optional[int] = 0
    pnl_lt_minus_dot5_num: Optional[int] = 0
    pnl_minus_dot5_0x_num: Optional[int] = 0
    pnl_lt_2x_num: Optional[int] = 0
    pnl_2x_5x_num: Optional[int] = 0
    pnl_gt_5x_num: Optional[int] = 0
    avg_holding_peroid: Optional[float] = 0
    profit_num: Optional[int] = 0
    token_avg_cost: Optional[float] = 0.0
    token_sold_avg_profit: Optional[float] = 0.0
    history_bought_cost: Optional[float] = 0.0
    winrate: Optional[float] = 0.0
    twitter_username: Optional[str] = None
    twitter_name: Optional[str] = None
    ens: Optional[str] = None
    avatar: Optional[str] = None
    name: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    tag_rank: TagRank = Field(default_factory=TagRank)
    refresh_requested_at: Optional[int] = None
    risk: Optional[Risk] = None


class WalletInfoResponse(BaseModel):
    code: int
    msg: str
    data: WalletInfo

    @property
    def wallet_data(self) -> WalletInfo:
        """
        Property to return the core wallet data.

        Returns:
            WalletInfo: The wallet data object.
        """
        return self.data

    def to_summary(self, wallet_address: str, summary_func: Optional[callable] = None) -> dict:
        """
        Summarizes wallet data. Returns the entire wallet data dictionary if no summary_func is provided.

        :param wallet_address: The address of the wallet.
        :param summary_func: Optional callable to customize the summary.
        :return: Dictionary summarizing the wallet data.
            Example:
                ...
                "buy_7d": 38,
                "sell_7d": 60,
                "buy": 38,
                "sell": 60,
                ...
        """

        if summary_func is not None:
            return summary_func(wallet_address, self.wallet_data)
        else:
            # return the entire dictionary, including wallet address
            # Adds "wallet_data" to the dictionary by using **
            return {"wallet_address": wallet_address, **self.wallet_data.model_dump()}