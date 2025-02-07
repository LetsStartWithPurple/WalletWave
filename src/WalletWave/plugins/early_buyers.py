from typing import List
from WalletWave.config import ConfigManager
from WalletWave.plugins.utils.plugin_interface import PluginInterface
from WalletWave.repositories.gmgn_repo import GmgnRepo
from WalletWave.utils.logging_utils import get_logger


# Author: viksant
# Version: 1.0.0

class EarlyBuyers(PluginInterface):
    """
    This plugin tends to retrieve the early byers of a token based on the token's CA

    Base Url: https://gmgn.ai/api/v1/token_trades/sol/<ContractAddress>?params...
    Real Url example: https://gmgn.ai/api/v1/token_trades/sol/4Z6AbaXT9nk5J3uihNSjBVUoxUTSosRbDTkTfAFMpump?device_id=eb337581-fb6a-48dd-9a37-b0a207b451f4&client_id=gmgn_web_2025.0207.224528&from_app=gmgn&app_ver=2025.0207.224528&tz_name=Europe%2FMadrid&tz_offset=3600&app_lang=%22en-US%22&limit=100&maker=&revert=true

    Useful Params (in the URL) for filtering data:
        # limit: How many traders will display. 100 by default
        # revert: if true, shows the first buyers of a given token. If false, the latest. Obviously, this should be true.

    Notes:
        - The overall point of this is retrieving the early buyers of a token, buy/sell txs and total profit they made.. the rest is unnecessary in my opinion.
        - Probably ask the users how many early traders does he want to retrieve: 50,100,150,200, etc (with a fixed amount & a limit)
    IMPORTANT: This retrieves only one buy/sell tx per time. A wallet can have many buys & sells at the same time..

    Url returns (most useful fields):
        "maker": "EmU3DGGxrGTh65XDBjetWDt5848b2n2GJ4n1u2bJBpTP", -> Wallet Address
        "base_amount": "18547961.44773400000000000000", -> How many tokens it bought/sold
        "quote_amount": "1.97668999700000000000", -> Tx value in Solana
        "amount_usd": "477.07413077595000000000", -> Sell tx value amount in Dolars
        "timestamp": 1737207340, -> When did he perform the TX
        "event": "sell",
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
    """
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.plugin_settings = config_manager.TokenEarlyBuyers
        self.gmgn = GmgnRepo()
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
        return "1.0.0"

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
                # Todo: ask the user to set the limit..
                user_input_ca = input("Enter Token's CA").strip()
                # Will handle mainly Pump.fun and Ray/Meteora tokens's length, which is 43-44 chars
                if len(user_input_ca) == 43 or len(user_input_ca) == 44:
                    contract_address = user_input_ca
                    break
                else:
                    # Todo: In the future, check if the CA is valid by using some Blockchain API calls.
                    #       DexScreener's API does suffice too, but has a 300 req/min limit.
                    #       For now, we'll assume that the pasted CA is correct.
                    self.logger.info(f"'{user_input_ca}' is invalid. Please enter a valid CA")

        except Exception as e:
            self.logger.critical(f"Config validation error: {e}")
            limit = 50
            revert = "true"
            self.logger.warning(f"Falling back to default values: limit={limit}")

        # 2. Fetch the data
        try:
            self.logger.info(f"Fetching early buyers with limit={limit}")
            early_buyers = await self.gmgn.get_early_buyers(contract_address, self.limit)
        except Exception as e:
            self.logger.critical(f"Error running plugin: {e}", exc_info=True)
            return []
    # 3. Analyze the data?
    # 4. Put it together
    # 5. Write it to output file
    async def finalize(self) -> None:
        self.logger.info("Solana Wallet Scanner finalized")