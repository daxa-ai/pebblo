"""
Module to handle logging functionality
"""
import logging


def get_logger():
    """Get uvicorn logger"""
    logger_obj = logging.getLogger("uvicorn.error")
    return logger_obj


logger = get_logger()
