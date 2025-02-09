from typing import List
from WalletWave.config import ConfigManager
from WalletWave.plugins.utils.plugin_interface import PluginInterface
from WalletWave.repositories.gmgn_repo import GmgnRepo
from WalletWave.utils.logging_utils import get_logger
from WalletWave.api.models.gmgn.early_buyers import EarlyBuyersResponse
from WalletWave.utils.dexscreener import DexScreener

from collections import defaultdict
import csv

# Author: viksant
# Version: 1.0.0

class EarlyBuyers(PluginInterface):
    """
    This plugin tends to retrieve the early byers of a token based on the token's CA

    Base Url: https://gmgn.ai/api/v1/token_trades/sol/<ContractAddress>?params...
    Real Url example: https://gmgn.ai/api/v1/token_trades/sol/4Z6AbaXT9nk5J3uihNSjBVUoxUTSosRbDTkTfAFMpump?device_id=eb337581-fb6a-48dd-9a37-b0a207b451f4&client_id=gmgn_web_2025.0207.224528&from_app=gmgn&app_ver=2025.0207.224528&tz_name=Europe%2FMadrid&tz_offset=3600&app_lang=%22en-US%22&limit=100&maker=&revert=true

    Useful Params (in the URL) for filtering data:
        # limit: How many traders will display. 100 by default
        # revert: if true, shows the first buyers of a given token. If false, the latest. Obviously, this should be always true.

    Notes:
        - The overall point of this is retrieving the early buyers of a token, buy/sell txs and total profit they made.. the rest is unnecessary in my opinion.
        - Probably ask the users how many early wallets/traders does he want to retrieve: 50,100,150,200, etc (with a fixed amount & a limit)

    IMPORTANT: This retrieves only one buy/sell tx per time. A wallet can have many buys & sells at the same time..

    Url returns (most useful fields):
        "maker": "EmU3DGGxrGTh65XDBjetWDt5848b2n2GJ4n1u2bJBpTP", -> Wallet Address
        "base_amount": "18547961.44773400000000000000", -> How many tokens it bought/sold
        "quote_amount": "1.97668999700000000000", -> Tx value in Solana
        "amount_usd": "477.07413077595000000000", -> Sell tx value amount in Dolars
        "timestamp": 1737207340, -> When did he perform the TX
        "event": "sell", -> Very important, as it determines what happened
        "total_trade": 2 -> How many txs did the wallet perform regarding the given token
        "buy_cost_usd": "389.95654670448000000000" -> Purchase price
        "balance": "0", -> Remaining tokens
        "history_bought_amount": "18547961.447734", -> Bought tokens (Would be good to put them in Millions for easier readability)
        "history_sold_amount": "18547961.447734", -> Sold tokens (Would be good to put them in Millions for easier readability)
        "realized_profit": "87.11758407147",
        "unrealized_profit": "0",
        "token_address": "J3TqbUgHurQGNxWtT88UQPcMNVmrL875pToQZdrkpump"

    Plugin will return a .csv file with:
        1. Buyers (in order)
        Note: should be nice to add how much time after token launch did they buy, even thought the buyers can be displayed in order based on buying timestamps filtering..
        2. Tokens bought
        3. Tokens sold
        4. How many buys it did
        5. How many sells it did
        6. Total Txs
        7. Realized Profit
        8. Unrealized Profit
        9. Total profit

    Important: Sometimes, within the established limits, we might miss a wallet's buy/sell.
    Example: This wallet -> 3LfX4Nm7ipyPs6p5jUEqdMpAihTchz9x6URjB9Dyk8L3 bought and sold once the token EH6SNJFmpLKo8oLuk3VMR7h1acg2tEvSzJwHDx51moon,
             but in the 50 limit, only shows a buy.. idk how to workaround this yet..
    """
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.plugin_settings = config_manager.TokenEarlyBuyers
        self.gmgn = GmgnRepo()
        self.ds = DexScreener("solana")
        # By default, 50 first early buyers will be fetched. User can configure it later on, but a limit should be established.
        self.limit = config_manager.get_plugin_setting(self.plugin_class, "limit", "50")
        self.logger = get_logger("Early Buyers")
        self.logger.debug("Initializing Early Buyers Plugin")

    def get_name(self) -> str:
        # return the name you want to show in the plugin menu
        return "Early Token Buyers"

    def get_description(self) -> str:
        # return a short description of your plugin
        return "Returns a given amount of early buyers of a specific Solana Token."

    def get_version(self) -> str:
        return "1.0.1"

    async def initialize(self) -> None:
        self.logger.info("Early Buyers plugin initialized.")

    async def execute(self) -> list:
        """
        Execute the plugin
        """

        # 1. Prepare the params for request
        contract_address = None
        try:
            limit = self.plugin_settings.get("limit")
            revert = self.plugin_settings.get("revert")
            while True:

                # Todo: Search alternatives to DexScreener's API, because it only shows tokens that are on dexscreener
                #       which means the ones that already migrated.. but what if the token just didn't migrate (yet)?
                user_input_ca = input("Enter Token's CA: ").strip()

                valid_ca = await self.ds.get_token_info_by_address(user_input_ca)

                if valid_ca and isinstance(valid_ca, list) and len(valid_ca) > 0 and "pairAddress" in valid_ca[0]:
                    contract_address = user_input_ca
                    print(f" Token address {user_input_ca} is valid. Continuing")
                    break
                else:
                    self.logger.info(f"'{user_input_ca}' is invalid. Please enter a valid CA")

        except Exception as e:
            self.logger.critical(f"Config validation error: {e}")
            limit = 50
            self.logger.warning(f"Falling back to default values: limit={limit}")

        # 2. Fetch the data
        try:
            self.logger.info(f"Fetching early buyers with limit={limit}")
            early_buyers = await self.gmgn.get_early_buyers(contract_address, self.limit)
            self._analyze_returned_buyers(early_buyers)
        except Exception as e:
            self.logger.critical(f"Error running plugin: {e}", exc_info=True)
            return []

    # 2. Analyze the data & Put it together
    def _analyze_returned_buyers(self, early_buyers: EarlyBuyersResponse) -> any:
        maker_stats = defaultdict(lambda: {
            'total_buys': 0,
            'total_sells': 0,
            'total_transactions': 0,
            'total_tokens_bought': 0.0,
            'total_tokens_sold': 0.0,
            'remaining_tokens': 0.0,
            'volume_buys_usd': 0.0,
            'volume_sells_usd': 0.0,
            'realized_profit': 0.0,
            'unrealized_profit': 0.0,
            'total_profit': 0.0,
            'roi': 0.0
        })
        if EarlyBuyersResponse:
            try:
                buyer_data_dictionary = defaultdict(list)
                # Group Transactions for each wallet
                for tx in early_buyers.buyer_data.history:
                    buyer_data_dictionary[tx.maker].append(tx)

                # Now, for each wallet, get their individual stats
                for wallet, transactions in buyer_data_dictionary.items():
                    for tx in transactions:
                        if tx.event == "buy":
                            maker_stats[wallet]['total_buys'] += 1
                            maker_stats[wallet]['total_transactions'] += 1
                            maker_stats[wallet]['total_tokens_bought'] += round(float(tx.base_amount), 2)
                            maker_stats[wallet]['volume_buys_usd'] += round(float(tx.amount_usd), 2)
                            maker_stats[wallet]['total_profit'] += round(float(tx.amount_usd), 2)
                        elif tx.event == "sell":
                            maker_stats[wallet]['total_sells'] += 1
                            maker_stats[wallet]['total_transactions'] += 1
                            maker_stats[wallet]['total_tokens_sold'] += round(float(tx.base_amount), 2)
                            maker_stats[wallet]['volume_sells_usd'] += round(float(tx.amount_usd), 2)
                            maker_stats[wallet]['total_profit'] -= round(float(tx.amount_usd), 2)

                        # Apparently, these numbers do not change based on tx.event
                        maker_stats[wallet]['realized_profit'] += round(float(tx.realized_profit), 2)
                        maker_stats[wallet]['unrealized_profit'] += round(float(tx.unrealized_profit), 2)
                        maker_stats[wallet]['total_profit'] = maker_stats[wallet]['realized_profit'] + maker_stats[wallet]['unrealized_profit']
                        if maker_stats[wallet]['volume_sells_usd'] > 0 and maker_stats[wallet]['volume_buys_usd'] > 0:
                            maker_stats[wallet]['roi'] = round((((maker_stats[wallet]['volume_buys_usd'] - maker_stats[wallet]['volume_sells_usd']) / maker_stats[wallet]['volume_buys_usd']) * 100), 2)
                        else:
                            maker_stats[wallet]['roi'] = 0
                # 3. Write it to output file
                fields = ['wallet', 'total_buys', 'total_sells', 'total_transactions', 'total_tokens_bought',
                          'total_tokens_sold',
                          'remaining_tokens', 'volume_buys_usd', 'volume_sells_usd', 'realized_profit',
                          'unrealized_profit',
                          'total_profit', 'roi']

                with open('earlyBuyers.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    for wallet, stats in maker_stats.items():
                        if maker_stats[wallet]["total_buys"] > 0 and maker_stats[wallet]["total_sells"]:
                            # Ignore those wallets who do not have sells but do have realized profit, as the sell Tx are not caught in this limit
                            writer.writerow({
                                'wallet': wallet,
                                **stats
                            })
                    self.logger.info("Early buyers data written to earlyBuyers.csv")
            except Exception as e:
                self.logger.critical(f"Error while parsing early buyers data: {e}")

    async def finalize(self) -> None:
        self.logger.info("Solana Wallet Scanner finalized")
