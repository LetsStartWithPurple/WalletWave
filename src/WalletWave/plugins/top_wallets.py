from typing import List

from WalletWave.config import ConfigManager
from WalletWave.plugins.utils.plugin_interface import PluginInterface
from WalletWave.repositories.gmgn_repo import GmgnRepo
from WalletWave.utils.config_validators import *
from WalletWave.utils.logging_utils import get_logger


# Author: LetsStartWithPurple
# Version: 2.0.0

def custom_summary(wallet_address, wallet_data):
    return {
        "wallet_address": wallet_address,
        "realized_profit": wallet_data.realized_profit,
        "buy": wallet_data.buy,
        "sell": wallet_data.sell,
        "total_value": wallet_data.total_value,
        "followers_count": wallet_data.followers_count,
        "winrate": wallet_data.winrate,
    }


class TopWallets(PluginInterface):

    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.plugin_settings = config_manager.TopWallets #dynamically get plugin settings
        self.gmgn = GmgnRepo()
        self.logger = get_logger("TopWallets")
        self.logger.debug("Initializing TOPWALLETS")

    def get_name(self) -> str:
        return "Top Wallets"

    def get_description(self) -> str:
        return "Plugin that gathers Top performing wallets"

    def get_version(self) -> str:
        return "2.0.0"

    async def initialize(self) -> None:
        self.logger.info("TopWallets plugin initialized.")

    async def execute(self) -> any:
        """
        Execute the plugin
        """
        try:
            timeframe = validate_timeframe(self.plugin_settings.get("timeframe"))
            wallet_tag = validate_wallet_tag(self.plugin_settings.get("wallet_tag"))
        except Exception as e:
            self.logger.critical(f"Config validation error: {e}")
            timeframe = "7d"
            wallet_tag = "smart_degen"
            self.logger.warning(f"Falling back to default values: timeframe={timeframe}, wallet_tag={wallet_tag}")

        try:
            # Step 1: Get the top wallets
            self.logger.debug(f"Fetching top wallets with params: timeframe={timeframe}, wallet_tag={wallet_tag}")
            top_wallets_response = await self.get_top_wallets(timeframe=timeframe, wallet_tag=wallet_tag)
            if not top_wallets_response:
                self.logger.error("No top wallets found.")
                return []

            self.logger.debug(f"Found {len(top_wallets_response)} top wallets to analyze")

            # Collect top wallets
            wallet_addresses = [wallet.wallet_address for wallet in top_wallets_response]


            # Step 2: Analyze each wallet activity
            wallet_information = await self.gmgn.get_wallet_info(wallet_addresses, period=timeframe)

            wallet_tuples = []
            for wallet_info, wallet_address in zip(wallet_information, wallet_addresses):
                if not wallet_info:
                    self.logger.warning(f"Skipping wallet {wallet_address} due to empty or invalid data")
                    continue

                # log wallet info summary
                self.logger.info(wallet_info.to_summary(wallet_address, summary_func=custom_summary))
                wallet_tuples.append((wallet_info, wallet_address))


            # Step 3: Filter wallets by winrate
            filtered_wallets = await self.filter_by_winrate(wallet_tuples)

            # log the result
            self.logger.info(f"Filtered {len(filtered_wallets)} wallets.")

            #rate limiter
            return filtered_wallets

        except Exception as e:
            self.logger.critical(f"Error running plugin: {e}", exc_info=True)
            return []

    async def finalize(self) -> None:
        self.logger.info("TopWallets plugin finalized")

    #custom function
    async def analyze_wallet_activity(self, wallet_address, period="7d"):
        """
        Analyze recent trading activity of a wallet using the getWalletInfo endpoint.

        :param wallet_address: Address of the wallet to analyze.
        :param period: Time period for wallet analysis (default "7d").
        :return: Wallet activity data.
        """
        self.logger.debug(f"Analyzing wallet {wallet_address} for period {period}")
        try:
            response = await self.gmgn.get_wallet_info(wallet_address=wallet_address, period=period)
            return response if response else None
        except Exception as e:
            self.logger.error(f"Error analyzing: {e}")

    #custom function
    async def get_top_wallets(self, timeframe="7d", wallet_tag="smart_degen"):
        """
        Fetch top performing wallets using the getTrendingWallets endpoint.

        :param timeframe: Time period for trending wallets (default "7d").
        :param wallet_tag: Tag to filter wallets (default "smart_degen").
        :return: List of top performing wallets.
        """
        self.logger.debug(f"Fetching trending wallets: timeframe={timeframe}, tag={wallet_tag}")
        try:
            response = await self.gmgn.get_trending_wallets(timeframe, wallet_tag)
            return response.rank if response else []
        except Exception as e:
            self.logger.error(f"Error fetching top wallets: {e}")

    # custom function
    async def filter_by_winrate(self, wallet_tuples: List[tuple]) -> List[dict]:
        """
        Filters wallets based on win rate and converts the result to a list of dictionaries.

        :param wallet_tuples: List of tuples (wallet_activity, wallet_address).
        :return: List of dictionaries with filtered wallet data.
        """

        try:
            user_defined_win_rate = validate_win_rate(self.plugin_settings.get("win_rate"))
        except Exception as e:
            self.logger.warning(f"Invalid win rate in setting: {e}")
            user_defined_win_rate = validate_win_rate(60)
            self.logger.info(f"Using default win rate: {user_defined_win_rate}")

        filtered_wallets = []

        self.logger.debug(f"Filtering wallets with win rate >= {user_defined_win_rate}")
        for wallet_activity, wallet_address in wallet_tuples:
            winrate = wallet_activity.wallet_data.winrate
            if winrate is not None and winrate >= user_defined_win_rate:
                wallet_dict = wallet_activity.to_summary(wallet_address)
                filtered_wallets.append(wallet_dict)
                self.logger.info(f"Wallet {wallet_address} passed with winrate: {winrate}.")
            else:
                self.logger.info(f"Wallet {wallet_address} failed with winrate: {winrate}.")

        return filtered_wallets
