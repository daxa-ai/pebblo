import json
from os import makedirs, path
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
    dir_path = path.dirname(file_path)

    # Create parent directories if needed
    makedirs(dir_path, exist_ok=True)

    try:
        with open(file_path, "w") as metadata_file:
            dump(data, metadata_file, indent=4, cls=DatetimeEncoder)  # Indent for readability
            logger.info(f"JSON data written successfully to: {file_path}")
    except Exception as e:
        logger.error(f"Error writing JSON data to file: {e}")


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logger.debug(f"Exception: File not found at path {file_path}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error: Unable to decode JSON in the file at path {file_path}")
        return None


def get_run_id():
    # Getting unique run id
    run_id = datetime.now().strftime("%m%d%Y_%H%M%S")
    return run_id
