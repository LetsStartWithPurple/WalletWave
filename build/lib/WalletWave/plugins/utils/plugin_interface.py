from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any

from WalletWave.config import ConfigManager


class PluginInterface(ABC):
    """
    Abstract base class for all plugins. Every plugin must implement the following methods.
    """

    def __init__(self, config_manager: ConfigManager):
        """
        Initializes the plugin with a ConfigManager instance.
        :param config_manager: The configuration manager for the plugin.
        """
        self.config_manager = config_manager
        self.plugin_class = self.__class__.__name__

    @abstractmethod
    def get_name(self) -> str:
        """
        Returns the name of the plugin.
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Returns a brief description of the plugin.
        """
        pass

    @abstractmethod
    def get_version(self) -> str:
        """
        Returns plugin version
        """
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """
        Called once to initialize the plugin with the given configuration.
        Plugins should fetch their configuration directly from the ConfigManager.
        """
        pass

    @abstractmethod
    async def execute(self) -> List[Union[Dict, Any]]:
        """
        Executes the plugin's main functionality.
        Plugins should handle all logic internally and return the processes data
        :return: Processed data.
        """
        pass

    @abstractmethod
    async def finalize(self) -> None:
        """
        Called when the plugin is being unloaded to clean up resources.
        """
        pass