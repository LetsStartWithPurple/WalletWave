from pydantic import BaseModel, ConfigDict
from enum import Enum

class ExportFormat(str, Enum):
    CSV = "csv"
    TXT = "txt"

class LogLevels(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ProgramSettings(BaseModel):
    """
    Pydantic model for validating configuration settings.
    Will only validate WalletWave specific settings. Does not validate plugin settings.
    Plugin validation will need to be created within the plugin itself.
    """
    model_config = ConfigDict(title="WalletWave Settings", extra='forbid')
    path: str = "data"
    export_format: ExportFormat = ExportFormat.CSV
    export_enabled: bool = True
    logging_level: LogLevels = LogLevels.INFO



