import logging
from pathlib import Path

from WalletWave.utils.settings.program_settings_model import ProgramSettings, LogLevels


class LogConfig:
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, log_level: LogLevels =None, log_dir: str ="logs", config: ProgramSettings = ProgramSettings):
        self.config = config
        self.log_level = self._get_log_level(log_level) if log_level is not None else self.config.logging_level
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self._configure_root_logger()

    def _get_log_level(self, default_level: LogLevels = LogLevels.INFO) -> LogLevels:
        if self.config:
            level = self.config.logging_level
            return level
        return default_level

    def _configure_root_logger(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level.value)
        root_logger.handlers.clear()
        
        # Handler to output logs to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            fmt=self.DEFAULT_FORMAT,
            datefmt=self.DEFAULT_DATE_FORMAT
        ))
        root_logger.addHandler(console_handler)

        try:
            # Handler to output logs to file app.log
            file_handler = logging.FileHandler(
                self.log_dir / "app.log"
            )
            
            file_handler.setFormatter(logging.Formatter(
                fmt=self.DEFAULT_FORMAT,
                datefmt=self.DEFAULT_DATE_FORMAT
            ))
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            console_handler.error(f"Failed to set up file logging: {e}")
            
    def get_gmgn_api_logger(self):
        logger = logging.getLogger('gmgn_api')
        file_handler = logging.FileHandler(self.log_dir / 'gmgn_api.log')
        file_handler.setFormatter(logging.Formatter(
            fmt=self.DEFAULT_FORMAT,
            datefmt=self.DEFAULT_DATE_FORMAT
        ))
        logger.addHandler(file_handler)
        return logger

def init_logging(config: ProgramSettings = None):
    LogConfig(config=config)

def get_logger(name):
    return logging.getLogger(name)
