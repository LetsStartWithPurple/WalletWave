from pydantic import BaseModel
from typing import Optional, List


class EarlyBuyers(BaseModel):
   maker: str
   base_amount: str
   quote_amount: str
   quote_symbol: str
   quote_address: str
   amount_usd: str
   timestamp: int
   event: str
   tx_hash: str
   price_usd: str
   total_trade: int
   id: str
   is_following: int
   is_open_or_close: int
   buy_cost_usd: str
   balance: str
   cost: str
   history_bought_amount: str
   history_sold_income: str
   history_sold_amount: str
   realized_profit: str
   unrealized_profit: str
   maker_tags: List[str]
   maker_token_tags: List[str]
   maker_name: str
   maker_twitter_username: str
   maker_twitter_name: str
   maker_avatar: str
   maker_ens: str
   token_address: str


class EarlyBuyersResponse(BaseModel):
    code: int
    msg: str
    data: EarlyBuyers

    @property
    def wallet_data(self) -> EarlyBuyers:
        """
        Property to return the core trading data.

        Returns:
            WalletInfo: The trade data object.
        """
        return self.data
