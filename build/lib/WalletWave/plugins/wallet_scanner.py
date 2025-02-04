from WalletWave.config import ConfigManager
from WalletWave.plugins.utils.plugin_interface import PluginInterface
from WalletWave.repositories.gmgn_repo import GmgnRepo
from WalletWave.utils.logging_utils import get_logger


# Author: LetsStartWithPurple
# Version: 1.0.1

class SolanaWalletScanner(PluginInterface):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.gmgn = GmgnRepo()
        self.timeframe = config_manager.get_plugin_setting(self.plugin_class, "timeframe", "7d")
        self.wallets = []
        self.logger = None        

    def get_name(self) -> str:
        # return the name you want to show in the plugin menu
        return "Solana Wallet Scanner"

    def get_description(self) -> str:
        # return a short description of your plugin
        return "Scans a list of wallets and exports performance"

    def get_version(self) -> str:
        return "1.0.1"

    async def initialize(self) -> None:
        # Step 1 of plugin lifecycle
        self.logger = get_logger("SolanaWalletScanner")
        self.logger.info("Solana Wallet Scanner initialized")

        # Loop until the user inputs the correct file path
        while True:
            wallet_file_path = input("Please provide the path to the wallet list file: ").strip()
            try:
                self._load_wallets(wallet_file_path)
                if not self.wallets:
                    self.logger.error("No wallets loaded. Stopping plugin execution")
                    raise RuntimeError("No wallets found in the specified file. Plugin cannot proceed")
                else:
                    self.logger.info(f"Solana Wallet Scanner initialized with {len(self.wallets)} wallets")
                    break
            except FileNotFoundError:
                print("The specified file does not exist. Check file path and try again.")
            except PermissionError:
                print("You don't have enough privileges to access this file. Please try again.")
            except Exception as e:
                print(f"An error occurred: {str(e)}. Please try again.")

    async def execute(self) -> list:
        while True:
            user_input = input("Type desired timeout between requests in seconds. Press 0 to omit: ").strip()
            try:
                timeout = int(user_input)

                if timeout < 0:
                    self.logger.info("Please enter a number 0 or greater.")
                    continue

                timeout = None if timeout == 0 else timeout
                break

            except ValueError:
                self.logger.info(f"'{user_input}' is invalid. Please enter a number 0 or greater")


        # Step 2 execute the plugin
        wallet_data = []
        self.logger.info("Executing Solana Wallet Scanner...")

        for wallet in self.wallets:
            try:
                wallet_info = await self.gmgn.get_wallet_info(wallet, timeout, period=self.timeframe)
                wallet_data.append(wallet_info.to_summary(wallet))
                self.logger.info(f"Fetched data for wallet: {wallet}")
            except Exception as e:
                self.logger.error(f"Error fetching data for wallet {wallet}: {e}")

        self.logger.info(f"Scanned {len(wallet_data)}")
        return wallet_data

    async def finalize(self) -> None:
        self.logger.info("Solana Wallet Scanner finalized")

    def _load_wallets(self, file_path: str) -> None:
        """
            Load wallets address from a text file
            :param file_path: Path to the text file containing wallets.
        """

        try:
            with open(file_path, 'r') as file:
                self.wallets = [line.strip() for line in file if line.strip()]
            self.logger.info(f"Loaded {len(self.wallets)} wallets from {file_path}.")
        except FileNotFoundError:
            self.logger.error(f"Wallet file not found: {file_path}")
        except Exception as e:
            self.logger.error(f"Error reading wallet file: {e}")
