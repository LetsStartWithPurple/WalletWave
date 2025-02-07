from pydantic import BaseModel, ConfigDict, ValidationError
from typing import Any, Dict, Type

# Registry: plugin name → configuration model.
plugin_config_registry: Dict[str, Type[BaseModel]] = {}

class PluginSettings(BaseModel):
    model_config = ConfigDict(title="Plugin Settings", extra="forbid")
    plugin_settings: Dict[str, Any] = {}

    @classmethod
    def register_plugin(cls, plugin_name: str, model: Type[BaseModel]) -> None:
        """
        Plugin developers call this to register their own configuration scheme.
        Todo: Cache the settings somehow
        """
        plugin_config_registry[plugin_name] = model

    @classmethod
    def validate_plugin_settings(cls, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        For each plugin configuration, if a registered model exists, validate the settings
        Otherwise, pass the settings along as-is
        """
        validated = {}
        for plugin, config in settings.items():
            if plugin in plugin_config_registry:
                try:
                    validated[plugin] = plugin_config_registry[plugin].model_validate(config)

                except ValidationError as e:
                    raise ValueError(f"Invalid configuration for plugin '{plugin}': {e}") from e
            else:
                validated[plugin] = config
        return validated


