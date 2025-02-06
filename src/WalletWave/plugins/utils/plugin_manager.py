import importlib
import inspect
import os
from pathlib import Path

from WalletWave.plugins.utils.plugin_interface import PluginInterface
from WalletWave.utils.logging_utils import get_logger


class PluginManager:
    """
    Manages plugins: loading, selecting, and executing them.
    """

    def __init__(self, config_manager=None):
        """
        Initialize the plugin manager with the directory containing plugins.
        """
        self.debug_logger = get_logger("PluginManager")

        root = Path(__file__).resolve().parent.parent

        self.plugin_directory = root
        self.debug_logger = get_logger(f"Plugins path is {self.plugin_directory}")
        self.config_manager = config_manager
        self.plugins = []

    def load_plugins(self) -> None:
        """
        Dynamically loads plugins from the specified directory.
        """
        self.debug_logger.debug(f"Plugin directory resolved to: {self.plugin_directory}")
        if not os.path.exists(self.plugin_directory):
            raise FileNotFoundError(f"Plugin directory does not exist: {self.plugin_directory}")

        for file in os.listdir(self.plugin_directory):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]  # Remove the .py extension
                try:
                    #Dynamically import the plugin
                    module = importlib.import_module(f"WalletWave.plugins.{module_name}")
                    for _, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, PluginInterface) and obj is not PluginInterface:
                            self.plugins.append(obj(self.config_manager))
                except Exception as e:
                    print(f"Failed to load plugin {module_name}: {e}")

    def list_plugins(self) -> None:
        """
        Lists all available plugins with their descriptions.
        """
        for i, plugin in enumerate(self.plugins):
            print(f"[{i + 1}] {plugin.get_name()} ({plugin.get_version()}): {plugin.get_description()}")

    def select_plugin(self, index: int):
        """
        Returns the selected plugin based on the index.
        """
        if 0 <= index < len(self.plugins):
            return self.plugins[index]
        else:
            raise ValueError("Invalid plugin index")
