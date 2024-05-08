"""
This module handles app prompt API business logic.
"""

from fastapi import HTTPException
from pydantic import ValidationError

from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.models.models import RetrievalData
from pebblo.app.utils.utils import (
    acquire_lock,
    read_json_file,
    release_lock,
    write_json_to_file,
)


class Prompt:
    """
    This class handles prompt API business logic.
    """

    def __init__(self, data: dict):
        self.data = data
        self.application_name = self.data.get("name")

    def _fetch_context_data(self, param):
        """
        Retrieve prompt/response data from input data and return its corresponding model object.
        """
        logger.debug(f"Retrieving {param} details from input data")

        data: dict = {}
        context_data = self.data.get(param)
        if context_data:
            data = {
                "data": context_data.get("data"),
                "entityCount": context_data.get("entityCount")
                if context_data.get("entityCount")
                else 0,
                "entities": context_data.get("entities")
                if context_data.get("entities")
                else {},
                "topicCount": context_data.get("topicCount")
                if context_data.get("topicCount")
                else 0,
                "topics": context_data.get("topics")
                if context_data.get("topics")
                else {},
            }
        logger.debug(f"AI_APPS [{self.application_name}]: {param} Details: {data}")
        return data

    def _create_retrieval_data(self):
        """
        Create an RetrievalData Model and return the corresponding model object
        """
        logger.debug("Creating RetrievalData model")
        retrieval_data_model = RetrievalData(**self.data)
        logger.debug(
            f"AI_APPS [{self.application_name}]: Retrieval Data Details: {retrieval_data_model.dict()}"
        )
        return retrieval_data_model

    @staticmethod
    def _write_file_content_to_path(file_content, file_path):
        """
        Write content to the specified file path.
        This function is just written for UT mocking.
        """
        logger.debug(f"Writing content to file path: {file_content}")
        # Writing file content to given file path
        write_json_to_file(file_content, file_path)

    @staticmethod
    def _read_file(file_path):
        """
        Retrieve the content of the specified file.
        This function is just written for UT mocking.
        """
        logger.debug(f"Reading content from file: {file_path}")
        file_content = read_json_file(file_path)
        return file_content

    def _upsert_app_metadata_file(self, retrieval_data):
        """
        Update/Create app_metadata file and write data for current retrieval
        """
        # Read app_metadata file & get current app_metadata
        app_metadata_file_path = (
            f"{CacheDir.HOME_DIR.value}/{self.application_name}"
            f"{CacheDir.APPLICATION_METADATA_FILE_PATH.value}"
        )
        app_metadata_lock_file = (
            f"{CacheDir.HOME_DIR.value}/"
            f"{self.application_name}"
            f"{CacheDir.APPLICATION_METADATA_LOCK_FILE_PATH.value}"
        )
        logger.debug(
            f"AI_APP [{self.application_name}]: app metadata file path: {app_metadata_file_path}"
        )
        try:
            acquire_lock(app_metadata_lock_file)

            # Read app_metadata file & get current app_metadata
            app_metadata_content = self._read_file(app_metadata_file_path)

            logger.debug(
                f"AI_APP [{self.application_name}]: app metadata content: {app_metadata_content}"
            )

            # write app_metadata file if it is not present
            if not app_metadata_content:
                app_metadata_content = {
                    "name": self.application_name,
                    "retrievals": [retrieval_data],
                }
            else:  # Updating retrieval data to file
                if "retrievals" in app_metadata_content.keys():
                    app_metadata_content.get("retrievals").append(retrieval_data)
                else:
                    app_metadata_content["retrievals"] = [retrieval_data]

            # Writing to app_metadata file
            self._write_file_content_to_path(
                app_metadata_content, app_metadata_file_path
            )
        finally:
            release_lock(app_metadata_lock_file)

    def process_request(self):
        """
        Process Prompt Request
        """
        try:
            logger.debug("AI App prompt request processing started")

            # Input Data
            logger.debug(f"AI_APP [{self.application_name}]: Input Data: {self.data}")

            # getting prompt data
            prompt_data = self._fetch_context_data("prompt")

            # getting response data
            response_data = self._fetch_context_data("response")

            self.data.update({"prompt": prompt_data, "response": response_data})

            # creating retrieval data model object
            retrieval_data = self._create_retrieval_data()

            self._upsert_app_metadata_file(retrieval_data.dict())

            logger.debug("AiApp prompt request completed successfully")
            return {"message": "AiApp Prompt Processed Successfully"}
        except ValidationError as ex:
            logger.error(f"Error in Prompt API process_request. Error:{ex}")
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            logger.error(f"Error in Prompt API process_request. Error:{ex}")
            raise HTTPException(status_code=500, detail=str(ex))
