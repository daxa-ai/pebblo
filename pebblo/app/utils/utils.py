import json
from os import makedirs, path
from json import JSONEncoder, dump
from pebblo.app.libs.logger import logger


class DatetimeEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


def write_json_to_file(data, file_path):
    try:
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
    home_dir = path.expanduser("~")
    full_file_path = path.join(home_dir, file_path)
    return full_file_path
