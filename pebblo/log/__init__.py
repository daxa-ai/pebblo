import logging
import logging.handlers
import os
from threading import Lock

from pebblo.app.config.config import var_server_config

g_config = var_server_config.get()

DEFAULT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class LoggerUtility:
    _lock = Lock()
    _loggers = {}

    def __new__(cls, *args, **kwargs):
        name = args[0]
        if not cls._loggers.get(name):
            with cls._lock:
                if not cls._loggers.get(name):
                    cls._loggers[name] = super(LoggerUtility, cls).__new__(cls)
                    cls._loggers[name]._initialize(*args, **kwargs)
        return cls._loggers[name]

    def _initialize(
        self, name, log_file, max_file_size, backup_count, level, timestamp_format
    ):
        self.logger = logging.getLogger(name)
        # self.logger.propagate = False
        self.logger.setLevel(level)
        self.log_file = log_file

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a file handler with log rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_file_size, backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
            datefmt=timestamp_format,
        )
        file_handler.setFormatter(file_formatter)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
            datefmt=timestamp_format,
        )
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


def get_logger(name: str):
    # Get logger from environment variables
    log_level = logging.getLevelName(g_config.logging.level.upper())
    log_file = g_config.logging.file
    log_max_file_size = g_config.logging.maxFileSize
    log_backup_count = g_config.logging.backupCount

    logger_utility = LoggerUtility(
        name,
        level=log_level,
        log_file=log_file,
        max_file_size=log_max_file_size,
        backup_count=log_backup_count,
        timestamp_format=DEFAULT_TIMESTAMP_FORMAT,
    )
    return logger_utility.get_logger()


def get_uvicorn_logconfig(log_file: str, log_level: int):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": log_file,
                "level": log_level,
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console", "file"],
                "level": log_level,
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
