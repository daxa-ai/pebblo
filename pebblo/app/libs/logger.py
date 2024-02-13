"""
Module to handle logging functionality
"""
import logging
from pebblo.app.daemon import config_details


def get_logger():
    """Get object of logger"""
    logger_level = config_details.get('logging', {}).get('level', 'info').upper()
    logger_obj = logging.getLogger("Pebblo Logger")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handle = logging.StreamHandler()
    console_handle.setFormatter(formatter)
    logger_obj.setLevel(logger_level)
    logger_obj.propagate = False
    if not logger_obj.handlers:
        logger_obj.addHandler(console_handle)
    return logger_obj


logger = get_logger()
