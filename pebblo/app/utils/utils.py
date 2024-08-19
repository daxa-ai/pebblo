import json
import time
from datetime import datetime
from json import JSONEncoder, dump
from os import getcwd, makedirs, path, remove
from shutil import rmtree

from fastapi import status

from pebblo.log import get_logger

logger = get_logger(__name__)


class DatetimeEncoder(JSONEncoder):
    def default(self, o):
        try:
            return super().default(o)
        except TypeError:
            return str(o)


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
            dump(data, metadata_file, indent=4, cls=DatetimeEncoder)
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
        with open(full_file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logger.debug(f"Exception: File not found at path {full_file_path}")
        return False
    except json.JSONDecodeError:
        logger.error(
            f"Error: Unable to decode JSON in the file at path {full_file_path}"
        )
        return False


def get_full_path(file_path):
    try:
        # path starting with '~'
        if file_path.startswith("~"):
            full_file_path = path.expanduser(file_path)
            return full_file_path
        # handle path starting with '.'
        if file_path.startswith("."):
            base_dir = getcwd()
            full_file_path = path.join(base_dir, file_path)
            return full_file_path
        # handle absolute path
        if file_path.startswith("/"):
            return file_path

        logger.error(f"Could not find {file_path} location.")
    except Exception as e:
        logger.error(
            f"Failed to figure out path for input : {file_path}. Exception: {e}"
        )


def delete_snippets(data):
    """
    Delete 'snippet' key from 'snippets' dictionary in 'findingsDetails'
    from the given data dictionary if they exist.

    """
    if data.get("findingsDetails") and len(data.get("findingsDetails")) > 0:
        for details in data.get("findingsDetails"):
            # Deleting snippet from dataSources
            if details.get("snippets") and len(details.get("snippets")) > 0:
                for snippet_detail in details.get("snippets"):
                    if snippet_detail.get("snippet"):
                        del snippet_detail["snippet"]

    return data


def update_findings_summary(data, app_name):
    """
    Update 'appName' key in 'findingsSummary' list in the given data dictionary
    with the value from the 'name' key of the app_json dictionary.
    """
    try:
        # Adding app name in findingsSummary
        if data.get("findingsSummary") and len(data.get("findingsSummary")) > 0:
            for finding_data in data.get("findingsSummary"):
                finding_data["appName"] = app_name
        logger.debug(f"Updated findingsSummary Data : {data}")
        return data.get("findingsSummary")

    except Exception as e:
        logger.warning(
            f"Error occurred while adding appName for data  : {data}. Exception: {e}"
        )
        return {}


def update_data_source(data, app_name, findings_entities, findings_topics):
    """
    Update the 'appName' key in the given data dictionary with the provided app_name.
    """
    try:
        updated_data: dict = dict()
        if not data:
            return updated_data

        # Create a new dictionary with updated values
        updated_data = {
            "appName": app_name,
            "name": data.get("name"),
            "sourcePath": data.get("sourcePath"),
            "sourceType": data.get("sourceType"),
            "sourceSize": data.get("sourceSize", 0),
            "totalSnippetCount": data.get("totalSnippetCount", 0),
            "displayedSnippetCount": data.get("displayedSnippetCount", 0),
            "findingsEntities": findings_entities,
            "findingsTopics": findings_topics,
        }
        logger.debug(f"Updated Data for dataSourceTab {updated_data}")
        return updated_data

    except Exception as e:
        logger.warning(
            f"Error occurred while updating dataSource for data  : {data}. Exception: {e}"
        )
        return {}


def get_document_with_findings_data(data):
    """
    Extracts data with findings information from the given data dictionary.
    """
    loader_data_list = []  # Initialize an empty list to store document data
    loader_info = data.get(
        "loaders"
    )  # Extract loader information from the data dictionary
    try:
        if loader_info:
            # Iterate over each loader in the loader_info
            for loader_data in loader_info:
                source_files = loader_data.get(
                    "sourceFiles"
                )  # Extract sourceFiles information
                if source_files:
                    # Iterate over each source file in the source_files
                    for source_file_details in source_files:
                        # Create a dictionary for each document with findings data
                        document_with_findings_data = {
                            "appName": data.get(
                                "name"
                            ),  # Get the app name from the data dictionary
                            "owner": data.get(
                                "owner"
                            ),  # Get the owner information from the data dictionary
                            "sourceName": loader_data.get(
                                "name"
                            ),  # Get the loader name
                            "sourceFilePath": source_file_details.get(
                                "name"
                            ),  # Get the source file path
                            "findingsEntities": source_file_details.get(
                                "findings_entities", 0
                            ),
                            # Get findings entities
                            "findingsTopics": source_file_details.get(
                                "findings_topics", 0
                            ),  # Get findings topics
                            "authorizedIdentities": source_file_details.get(
                                "authorized_identities", []
                            ),  # Get authorized identities
                            "lastModified": loader_data.get(
                                "lastModified"
                            ),  # Get the last modified timestamp
                        }
                        loader_data_list.append(
                            document_with_findings_data
                        )  # Append the document data to the list
    except Exception as err:
        # Handle any exceptions and print the error message
        logger.warning(f"Error occurred: {str(err)}")
    return loader_data_list  # Return the list of document data


def get_pebblo_server_version():
    """Fetch local pebblo server version"""
    import importlib.metadata

    __version__ = importlib.metadata.version("pebblo")
    return __version__


def acquire_lock(lock_file_path: str):
    """
    Acquire lock using given lock file. It will be busy wait, polling after every 2 seconds.
    """
    sleep_time = 2
    while True:
        try:
            full_lock_file_path = get_full_path(lock_file_path)

            # Extract directory path from the lock file path
            lock_dir = path.dirname(full_lock_file_path)

            # Create directory if it doesn't exist
            if not path.exists(lock_dir):
                makedirs(lock_dir)

            # Try to open the file in write mode exclusively.
            # This will create the file if it doesn't exist and fail if it does.
            with open(full_lock_file_path, "x"):
                # If successful, break out of the loop
                logger.debug(f"Lock Acquired. {full_lock_file_path}")
                break
        except FileExistsError:
            # If the file already exists, wait for a short while and try again
            logger.debug(f"Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)


def release_lock(lock_file_path: str):
    """
    Release lock for given lock file.
    """
    # Simply delete the lock file to release the lock
    try:
        full_lock_file_path = get_full_path(lock_file_path)
        remove(full_lock_file_path)
        logger.debug(f"Lock Released. {full_lock_file_path}")
    except FileNotFoundError:
        pass  # The lock file doesn't exist, nothing to release


def delete_directory(app_path, app_name=None):
    message = ""
    result = {}
    try:
        full_path = get_full_path(app_path)
        logger.info(f"DirPath: {full_path}")
        rmtree(full_path)
        message = f"Application {app_name} has been deleted."
        logger.info(message)
        result = {"message": message, "status_code": status.HTTP_200_OK}
    except FileNotFoundError:
        message = f"Application {app_name} does not exist."
        result = {"message": message, "status_code": status.HTTP_404_NOT_FOUND}
        logger.exception(message)
    except PermissionError:
        message = f"Permission denied: Unable to delete application {app_name}."
        result = {
            "message": message,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        }
        logger.exception(message)
    except Exception as e:
        message = f"Unable to delete application {app_name}, Error: {e}"
        result = {
            "message": message,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
        logger.exception(message)
    finally:
        return result


def get_current_time():
    """
    Return current time in isoformat
    :return:
    """
    return datetime.now().isoformat()


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        response = func(*args, **kwargs)
        end_time = time.perf_counter()
        logger.debug(
            f"Execution time of function <{func.__name__}> is {end_time-start_time} seconds."
        )
        return response

    return wrapper
