import os
import pathlib

# Default config value
dir_path = pathlib.Path().absolute()


# Logging Defaults
DEFAULT_LOGGER_NAME = "pebblo"
DEFAULT_LOG_MAX_FILE_SIZE = 8 * 1024 * 1024
DEFAULT_LOG_BACKUP_COUNT = 3
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FILE_PATH = "/tmp/logs"
DEFAULT_LOG_FILE = f"{DEFAULT_LOG_FILE_PATH}/{DEFAULT_LOGGER_NAME}.log"


# set shared variable to verify if anonymizeSnippets is either in classifier or reports
anonymize_snippets_exists = False


def update_anonymize_snippets_exists():
    # Update anonymize_snippets_exists value to True if anonymize_snippets_exists is already in reports
    global anonymize_snippets_exists
    anonymize_snippets_exists = True


def expand_path(file_path: str) -> str:
    # Expand user (~) and environment variables
    expanded_path = os.path.expanduser(file_path)
    expanded_path = os.path.expandvars(expanded_path)

    # Convert to absolute path
    absolute_path = os.path.abspath(expanded_path)

    return absolute_path
