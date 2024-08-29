"""
This module handles app prompt API business logic.
"""

from pydantic import ValidationError

from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import (
    PromptResponseModel,
    RetrievalContext,
    RetrievalData,
)
from pebblo.app.utils.utils import (
    acquire_lock,
    read_json_file,
    release_lock,
    write_json_to_file,
)
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger
from pebblo.topic_classifier.topic_classifier import TopicClassifier

logger = get_logger(__name__)


class Prompt:
    """
    This class handles prompt API business logic.
    """

    def __init__(self):
        self.data = None
        self.application_name = None
        self.entity_classifier_obj = EntityClassifier()
        self.topic_classifier_obj = TopicClassifier()

    def _initialize_data(self, data):
        self.data = data
        self.application_name = data.get("name")

    def _fetch_classified_data(self, input_data, input_type=""):
        """
        Retrieve input data and return its corresponding model object with classification.
        """
        logger.debug(f"Retrieving details for: {input_type}")

        (
            entities,
            entity_count,
            _,
            _,
        ) = self.entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
            input_data
        )

        data = {"data": input_data, "entityCount": entity_count, "entities": entities}

        # Topic classification is performed only for the response.
        if input_type == "response":
            topics, topic_count, topic_details = self.topic_classifier_obj.predict(
                input_data
            )
            data["topicCount"] = topic_count
            data["topics"] = topics

        return data

    def _create_retrieval_data(self, context_data):
        """
        Create an RetrievalData Model and return the corresponding model object
        """
        logger.debug(f"Creating RetrievalData model: {self.data}")
        retrieval_data_model = RetrievalData(**self.data)
        retrieval_data_model.context = context_data
        logger.debug(
            f"AI_APPS [{self.application_name}]: Retrieval Data Details: {retrieval_data_model.model_dump()}"
        )
        return retrieval_data_model

    @staticmethod
    def _write_file_content_to_path(file_content, file_path):
        """
        Write content to the specified file path.
        This function is just written for UT mocking.
        """
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

    def process_request(self, data):
        """
        Process Prompt Request
        """
        self._initialize_data(data)
        try:
            logger.debug("AI App prompt request processing started")

            # getting prompt data
            prompt_data = self.data.get("prompt", {})

            is_prompt_gov_enabled = self.data.get("prompt", {}).get(
                "prompt_gov_enabled", False
            )

            if is_prompt_gov_enabled is False:
                prompt_data = self._fetch_classified_data(
                    prompt_data.get("data", ""), input_type="prompt"
                )

            # getting response data
            response_data = self._fetch_classified_data(
                self.data.get("response", {}).get("data"), input_type="response"
            )

            # getting retrieval context data
            context_data = self._fetch_context_data(self.data.get("context"))

            self.data.update({"prompt": prompt_data, "response": response_data})

            # creating retrieval data model object
            retrieval_data = self._create_retrieval_data(context_data)

            self._upsert_app_metadata_file(retrieval_data.model_dump())

            message = "AiApp prompt request completed successfully"
            logger.debug(message)
            response = PromptResponseModel(retrieval_data=self.data, message=message)
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=200
            )
        except ValidationError as ex:
            response = PromptResponseModel(retrieval_data=None, message=str(ex))
            logger.error(f"Error in Prompt API process_request. Error: {ex}")
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=400
            )
        except Exception as ex:
            response = PromptResponseModel(retrieval_data=None, message=str(ex))
            logger.error(f"Error in Prompt API process_request. Error: {ex}")
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=500
            )

    @staticmethod
    def _fetch_context_data(context_list):
        retrieval_context_data = []
        if context_list:
            for context in context_list:
                retrieval_context_obj = RetrievalContext(
                    retrieved_from=context.get("retrieved_from"),
                    doc=context.get("doc"),
                    vector_db=context.get("vector_db"),
                )
                retrieval_context_data.append(retrieval_context_obj)
        return retrieval_context_data
