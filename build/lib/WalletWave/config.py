import argparse
import os

import yaml
from yaml import YAMLError

from WalletWave.utils.config_validators import *
from WalletWave.utils.logging_utils import get_logger


class ConfigManager:
    """
    Wallet Wave configuration manager!

    This class is responsible for:
      - Loading and parsing the YAML configuration file
      - Merging the config settings with command-line args
      - Managing plugin-specific settings.
    """
    def __init__(self, args = None):
        """
        Init the Config Manager

        :param args: Command-line arguments parsed via argparse
        """
        self.logger = get_logger("ConfigManager") # set global logger
        self._config_path = os.path.abspath(args.config) # get absolute path of the config file
        self._config_data = self._load_config() # load the config from YAML file
        self._args = args # store the command line args
        self._final_config = self._merge_configurations() # merge the file config settings with the CLI arguments
        self._plugin_settings = self._load_plugin_settings() # load plugin settings

    def _load_config(self):
        """
        Load the configuration file

        :return: Parsed YAML data as dict
        """
        try:
            with open(self._config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file: '{self._config_path}' not found. Using defaults")
            return {}
        except YAMLError as e:
            self.logger.error(f"Failed to parse YAML in config file '{self._config_path}': {e}")
            return {}


    def _merge_configurations(self):
        """
        Config file and command-line arguments merger

        Command line args take precedence over config file settings

        :return: A dictionary containing the final merged configuration


        """
        program_settings = self._config_data.get("program_settings", {})
        return {
            "export_path": validate_path(
                self._args.export_path if self._args and self._args.export_path else program_settings.get("export_path", "data")
            ),
            "export_format": validate_export_format(
                self._args.export_format if self._args and self._args.export_format else program_settings.get("export_format", "csv")
            ),
            "export_enabled": validate_export_enabled(
              program_settings.get("export_enabled", True) #defaults to True
            ),
            "logging_level": program_settings.get("logging_level", "INFO")
        }

    def _load_plugin_settings(self):
        """
        Load plugin-specific settings from the config file

        :return: Dictionary containing plugin configs
        """
        plugins = self._config_data.get("plugin_settings", {})
        return {plugin: settings for plugin, settings in plugins.items()}

    @property
    def plugins(self):
        """ Return all plugin settings as dict """
        return self._plugin_settings

    def get_plugin_setting(self, plugin, key, default=None):
        """
        Get a specific setting for a plugin
        :param plugin: Name of the plugin
        :param key: Setting key within the plugin config file
        :param default: Default value if the setting is not found
        :return: Value of the requested setting or the default
        """
        return self._plugin_settings.get(plugin, {}).get(key, default)

    def set_plugin_setting(self, plugin, key, value):
        """
        Set a specific setting for a plugin

        :param plugin: Name of the plugin
        :param key: Setting key to update
        :param value: New value for the setting
         """
        if plugin not in self._plugin_settings:
            self._plugin_settings[plugin] = {}
        self._plugin_settings[plugin][key] = value

    def __getattr__(self, name):
        """
        Dynamic attribute access to plugin settings

        If a plugin setting does not exist, return an empty dict and log warning

        :param name: Plugin name
        :return: Plugin settings as a dict or an empty dict if not found
        """
        if name in self._plugin_settings:
            return self._plugin_settings[name]
        self.logger.warning(f"No plugin settings with {name} found, proceeding without plugin settings")
        return {}


    # --- CONFIGURATION PROPERTIES ---

    @property
    def export_path(self):
        """ Return the export path setting. """
        return self._final_config["export_path"]

    @export_path.setter
    def export_path(self, new_path):
        """ Set and validate a new export path """
        self._final_config["export_path"] = validate_path(new_path)

    @property
    def verbose(self):
        """ Return the verbose setting (logging level) """
        return self._final_config["verbose"]

    @verbose.setter
    def verbose(self, verbose):
        """ Set and validate the verbose mode setting """
        self._final_config["verbose"] = validate_verbose(verbose)

    @property
    def export_format(self):
        """ Return the export format setting. """
        return self._final_config["export_format"]

    @export_format.setter
    def export_format(self, export_format):
        """ Set and validate a new export format"""
        self._final_config["export_format"] = validate_export_format(export_format)

    @property
    def export_enabled(self):
        """ Return whether exporting is enabled. """
        return self._final_config["export_enabled"]

    @property
    def config(self):
        """ Return the fully merged config dictionary """
        return self._final_config

def parse_args():
    """ Parse command-line arguments"""
    # Get the default path of the config file relative the script directory
    default_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yaml"))

    parser = argparse.ArgumentParser(description="Smart Money Follower Configuration")
    parser.add_argument("--config", type=str, default=default_config_path, help="Path to the config file")
    parser.add_argument("--export_path", type=str, help="Path to export files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--export-format", type=str, choices=["csv", "txt"], help="Export format (csv or txt)")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse arguments
    args = parse_args()
    args.config = "config.yaml" # for testing purposes

    # Create ConfigManager instance
    config_manager = ConfigManager(args=args)

    # Access properties
    print("Final Configuration:")
    print(f"Export Path: {config_manager.export_path}")
    print(f"Export Format: {config_manager.export_format}")

    #plugin settings
    # get via attributes
    plugin_settings = config_manager.TopWallets
    print(plugin_settings.get("timeframe"))

    # get directly
    plugin_settings = config_manager.get_plugin_setting("TopWallets", "timeframe")
    print(plugin_settings)

