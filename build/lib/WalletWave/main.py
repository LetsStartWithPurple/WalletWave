from CLI.menu import menu
from WalletWave.config import parse_args
from WalletWave.config import ConfigManager
from WalletWave.utils.file_utils import FileUtils
from WalletWave.utils.logging_utils import get_logger, init_logging
import asyncio

class WalletWave:
    """
    Main class that handles plugin execution and data export
    - execute function of WalletWave
       - Step 1: Initialize the plugin
       - Step 2: Execute the plugin
       - Step 3: Export plugin results
       - Step 4: Finalize the plugin
    - export function
       - Exports the data returned from plugin by passing to file_utils
    """
    def __init__(self, config: ConfigManager):
        """
        Initializes the main app.
        """
        self.config = config
        self.logger = get_logger("WalletWave")
        self.file_utils = FileUtils(self.config.export_path)

    async def execute(self, plugin):
        """
        Executes the selected plugin's lifecycle: initialize, execute, and finalize.
        :param plugin: The plugin object to execute.
        """
        try:
            # Step 1: Initialize the plugin
            self.logger.info(f"Initializing: {plugin.get_name()}")
            await plugin.initialize()

            # Step 2: Execute the plugin
            self.logger.info("Executing plugin...")
            data = await plugin.execute()

            # Step 3: Export plugin results
            if self.config.export_enabled:
                self.logger.info("Exporting plugin results..")
                self.export_data(data)
            else:
                self.logger.info("Exporting data has been set to False in the config file. Skipping export function.")

            # Step 4: Finalize the plugin
            self.logger.info("Finalizing plugin...")
            await plugin.finalize()
        except Exception as e:
            self.logger.error(f"An error occurred while running the plugin: {e}")

    def export_data(self, data, export_format = 'csv'):
        """
        Wrapper method to export data using FileUtils.
        """
        self.logger.info("Exporting wallet data...")
        self.file_utils.export_wallet_data(data, export_format=export_format)


def main():
    """
    Application entry point that handles:
      - Command line argument parsing
      - Configuration management
      - Logging initialization
      - Menu interaction
      - Plugin execution
    """
    try:
        # Parse command line arguments (config.py - parse_args())
        args = parse_args()

        # Initialize configuration manager (config.py)
        manager = ConfigManager(args)

        # Setup logging based on config
        # Passes configuration settings to logging_utils
        init_logging(manager.config)

        # Display menu and get user selection
        # CLI - menu.py
        action = menu(manager)

        # exit if prompted
        if action == "exit":
            return

        # Create main application instance (main.py - WalletWave::class)
        app = WalletWave(manager)

        # Extract the selected plugin from menu action
        # menu.py returns ["plugin", selected_plugin] to action variable
        selected_plugin = action[1]

        # Execute the selected plugin asynchronously
        asyncio.run(app.execute(selected_plugin))
    except ValueError as e:
        exit(1)

if __name__ == "__main__":
    main()