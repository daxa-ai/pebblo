"""
Module for text classification
"""

import traceback

from pydantic import ValidationError

from pebblo.app.api.req_models import ReqClassifier
from pebblo.app.config.config import var_server_config_dict
from pebblo.app.enums.common import ClassificationMode
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import AiDataModel
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger
from pebblo.topic_classifier.topic_classifier import TopicClassifier

config_details = var_server_config_dict.get()


logger = get_logger(__name__)
topic_classifier_obj = TopicClassifier()
entity_classifier_obj = EntityClassifier()


class Classification:
    """
    Classification wrapper class for Entity and Semantic classification with anonymization
    """

    def __init__(self, data: dict):
        self.input = data

    @staticmethod
    def _get_classifier_response(req: ReqClassifier):
        """
        Processes the input prompt through the entity classifier and anonymizer, and returns
        the resulting information encapsulated in an AiDataModel object.

        Returns:
            AiDataModel: An object containing the anonymized document, entities, and their counts.
        """
        doc_info = AiDataModel(
            data=None,
            entities={},
            entityCount=0,
            entityDetails={},
            topics={},
            topicCount=0,
            topicDetails={},
        )
        try:
            # Process entity classification
            if req.mode in [
                ClassificationMode.ENTITY,
                ClassificationMode.ALL,
            ]:
                (
                    entities,
                    entity_count,
                    anonymized_doc,
                    entity_details,
                ) = entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
                    req.data,
                    anonymize_snippets=req.anonymize,
                )
                doc_info.entities = entities
                doc_info.entityCount = entity_count
                doc_info.entityDetails = entity_details
                doc_info.data = anonymized_doc if req.anonymize else ""

            # Process topic classification
            if req.mode in [
                ClassificationMode.TOPIC,
                ClassificationMode.ALL,
            ]:
                topics, topic_count, topic_details = topic_classifier_obj.predict(
                    req.data
                )
                doc_info.topics = topics
                doc_info.topicCount = topic_count
                doc_info.topicDetails = topic_details
            return doc_info
        except (KeyError, ValueError, RuntimeError) as e:
            logger.error(f"Failed to get classifier response: {e}")
            return doc_info
        except Exception as e:
            logger.error(f"Unexpected error:{e}\n{traceback.format_exc()}")
            return doc_info

    def process_request(self):
        """
        Processes the user request for classification and returns a structured response.

        Returns:
            PebbloJsonResponse: The response object containing classification results or error details.
        """
        try:
            req = ReqClassifier.model_validate(self.input)
            if not req.data:
                return PebbloJsonResponse.build(
                    body={"error": "Input data is missing"}, status_code=400
                )
            doc_info = self._get_classifier_response(req)
            return PebbloJsonResponse.build(
                body=doc_info.model_dump(exclude_none=True), status_code=200
            )
        except ValidationError as e:
            logger.error(
                f"Validation error in Classification API process_request:{e}\n{traceback.format_exc()}"
            )
            return PebbloJsonResponse.build(
                body={"error": f"Validation error: {e}"}, status_code=400
            )
        except Exception:
            response = AiDataModel(
                data=None,
                entities={},
                entityCount=0,
                topics={},
                topicCount=0,
                topicDetails={},
            )
            logger.error(
                f"Error in Classification API process_request: {traceback.format_exc()}"
            )
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=500
            )
