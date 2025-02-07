from pydantic import BaseModel, ConfigDict
from WalletWave.utils.settings.program_settings_model import ProgramSettings
from typing import Any, Dict

class BaseSettings(BaseModel):
    model_config = ConfigDict(title="Base Settings Model", extra='forbid')
    program_settings: ProgramSettings
    plugin_settings: Dict[str, Any] = {}