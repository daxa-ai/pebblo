"""
Module to handle logging functionality
"""
import logging

LOG_LEVELS = {}


def get_logger():
    """Get uvicorn logger"""
    global LOG_LEVELS
    LOG_LEVELS = logging._nameToLevel
    logger_obj = logging.getLogger("uvicorn.error")
    return logger_obj


logger = get_logger()

SUPPORTED_LOG_LEVELS = LOG_LEVELS