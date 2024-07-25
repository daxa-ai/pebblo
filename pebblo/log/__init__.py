import logging
import logging.handlers
import os
from threading import Lock

from pebblo.app.config.config import DEFAULT_LOG_FILE, DEFAULT_LOG_LEVEL, DEFAULT_LOG_MAX_FILE_SIZE, DEFAULT_LOG_BACKUP_COUNT, DEFAULT_LOGGER_NAME

DEFAULT_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

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

    def _initialize(self, name, log_file, max_file_size, backup_count, level, timestamp_format):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.log_file = log_file

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a file handler with log rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_file_size, backupCount=backup_count)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            f'%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', datefmt=timestamp_format)
        file_handler.setFormatter(file_formatter)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            f'%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', datefmt=timestamp_format)
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

def get_logger(name:str):
    # Get logger from environment variables
    log_level = logging.getLevelName(os.environ.get('LOG_LEVEL', DEFAULT_LOG_LEVEL))
    log_file = os.environ.get('LOG_FILE', DEFAULT_LOG_FILE)
    log_max_file_size = int(os.environ.get('LOG_MAX_FILE_SIZE', str(DEFAULT_LOG_MAX_FILE_SIZE)))
    log_backup_count = int(os.environ.get('LOG_BACKUP_COUNT', str(DEFAULT_LOG_BACKUP_COUNT)))

    logger_utility = LoggerUtility(name, level=log_level, log_file=log_file, max_file_size=log_max_file_size, backup_count=log_backup_count, timestamp_format=DEFAULT_TIMESTAMP_FORMAT)
    return logger_utility.get_logger()

def get_uvicorn_logconfig(log_file:str, log_level:int):
    '''
    Log config in logging.config.dictConfig format for uvicorn framework
    '''
    log_config = {
        "version": 1,
        'disable_existing_loggers': False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(process)s - %(name)s - %(levelname)s - %(message)s",
            },
            "json": {
                "()": "stdlib.log.CustomUvironJsonFormatter",
            }
        },
        "handlers": {
            "default_console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "level": "DEBUG"
            },
            "console": {
                "formatter": "json",
                "class": "logging.StreamHandler",
                "level": log_level,
            },
        },
        "root": {
                "handlers": ["console"],
                "level": log_level,
        },
        "loggers": {
            "gunicorn": {
                "propagate": True,
            },
            "uvicorn": {
                "propagate": True,
            },
            "uvicorn.access": {
                "propagate": True,
            }
        }
    }
    if log_file != None:
        try:
            f = open(log_file, "a")
            f.close()
            log_config["handlers"]["file"] = {
                "formatter": "json",
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "filename": log_file,
            }
            log_config["root"]["handlers"].append("file")
        except Exception as e:
            # silently disable file handler if log file not writable
            pass
    return log_config


if __name__ == '__main__':
    logger = get_logger("test")

    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

    logger = get_logger("test-123")

    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")