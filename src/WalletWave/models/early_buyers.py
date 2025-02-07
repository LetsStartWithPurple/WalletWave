from pydantic import BaseModel

from typing import Optional, List

class EarlyBuyersEntry(BaseModel):
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

   """
   Todo: Check some tags that are returned as arrays
        1. maker_tags -> Search for wallet that does indeed have these tags and see if they are key:value or is just a list..
        
   Example output 
   {
    "maker": "2keaRYY2tc1evtoXqi2YibMyDZZm4Foo4Hxy974dMZfe",
    "base_amount": "536499999.99999900000000000000",
    "quote_amount": "30.00000000000000000000",
    "quote_symbol": "SOL",
    "quote_address": "So11111111111111111111111111111111111111111",
    "amount_usd": "5921.70000000000000000000",
    "timestamp": 1738925038,
    "event": "buy",
    "tx_hash": "4RJ89Qixa8YrHkUZuB2ttrXo3oJ739jYxyV9SoL8zGHkZhVC46QJwaRXGY7b7VVHs3L54coteH3Jobs3m3BbQome",
    "price_usd": "0.00001103765145393000",
    "total_trade": 1,
    "id": "MDAzMTkwNTY0MzgxNjU3MDAwNQ==",
    "is_following": 0,
    "is_open_or_close": 1,
    "buy_cost_usd": "",
    "balance": "1113.174177",
    "cost": "0.01228682856279759979",
    "history_bought_amount": "536499999.999999",
    "history_sold_income": "0",
    "history_sold_amount": "0",
    "realized_profit": "0",
    "unrealized_profit": "2.66594634510144260021",
    "maker_tags": [],
    "maker_token_tags": [
      "creator",
      "sniper"
    ],
    "maker_name": "",
    "maker_twitter_username": "",
    "maker_twitter_name": "",
    "maker_avatar": "",
    "maker_ens": "",
    "token_address": "4Z6AbaXT9nk5J3uihNSjBVUoxUTSosRbDTkTfAFMpump"
      },
   """


class WalletInfoResponse(BaseModel):
    code: int
    reason: str
    message: str
    data: EarlyBuyersEntry

    @property
    def wallet_data(self) -> EarlyBuyersEntry:
        """
        Property to return the core transaction data.

        Returns:
            EarlyBuyersEntry: The trade data object.
        """
        return self.data