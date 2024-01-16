import json
from os import makedirs, path, name
from datetime import datetime
from json import JSONEncoder, dump
from libs.logger import logger


class DatetimeEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


def write_json_to_file(data, file_path):
    home_dir = path.expanduser("~")

    # Construct the full path based on the operating system
    if name == "nt":  # For windows Operating System
        full_file_path = path.join(home_dir, file_path.replace('/', '\\'))
    else:
        full_file_path = path.join(home_dir, file_path)

    # Create parent directories if needed
    dir_path = path.dirname(full_file_path)
    makedirs(dir_path, exist_ok=True)

    try:
        with open(full_file_path, "w") as metadata_file:
            dump(data, metadata_file, indent=4, cls=DatetimeEncoder)  # Indent for readability
            logger.info(f"JSON data written successfully to: {full_file_path}")
    except Exception as e:
        logger.error(f"Error writing JSON data to file: {e}")


def read_json_file(file_path):
    home_dir = path.expanduser("~")
    try:
        # Construct the full path based on the operating system
        if name == "nt":  # For windows Operating System
            full_file_path = path.join(home_dir, file_path.replace('/', '\\'))
        else:
            full_file_path = path.join(home_dir, file_path)
        with open(full_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logger.debug(f"Exception: File not found at path {full_file_path}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error: Unable to decode JSON in the file at path {full_file_path}")
        return None


def get_run_id():
    # Getting unique run id
    run_id = datetime.now().strftime("%m%d%Y_%H%M%S")
    return run_id
