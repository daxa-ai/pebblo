import json
from os import makedirs, path, getcwd
from json import JSONEncoder, dump
from pebblo.app.libs.logger import logger


class DatetimeEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


def write_json_to_file(data, file_path):
    """
        Write content to the specified file path
    """
    try:
        # Writing file content to given file path
        logger.debug(f"Writing content to file path: {file_path}")
        full_file_path = get_full_path(file_path)
        # Create parent directories if needed
        dir_path = path.dirname(full_file_path)
        makedirs(dir_path, exist_ok=True)
        with open(full_file_path, "w") as metadata_file:
            dump(data, metadata_file, indent=4, cls=DatetimeEncoder)  # Indent for readability
            logger.debug(f"JSON data written successfully to: {full_file_path}")
    except Exception as e:
        logger.error(f"Error writing JSON data to file: {e}")


def read_json_file(file_path):
    """
        Retrieve the content of the specified file.
    """
    logger.debug(f"Reading content from file: {file_path}")
    full_file_path = ""
    try:
        full_file_path = get_full_path(file_path)
        with open(full_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logger.debug(f"Exception: File not found at path {full_file_path}")
        return False
    except json.JSONDecodeError:
        logger.error(f"Error: Unable to decode JSON in the file at path {full_file_path}")
        return False


def get_full_path(file_path):
    try:
        # path starting with '~'
        if file_path.startswith("~"):
            full_file_path = path.expanduser(file_path)
            return full_file_path
        # handle path starting with '.'
        elif file_path.startswith("."):
            base_dir = getcwd()
            full_file_path = path.join(base_dir, file_path)
            return full_file_path
        # handle absolute path
        elif file_path.startswith("/"):
            return file_path
        # error case
        else:
            logger.error(f"Could not find {file_path} location.")
    except Exception as e:
        logger.error(f"Failed to figure out path for input : {file_path}. Exception: {e}")