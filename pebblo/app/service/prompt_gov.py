"""
Module for prompt governance
"""

import traceback

from pydantic import ValidationError

from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import AiDataModel, PromptGovResponseModel
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger

logger = get_logger(__name__)


class PromptGov:
    """
    Class for loader doc related task
    """

    def __init__(self, data):
        self.input = data
        self.entity_classifier_obj = EntityClassifier()

    def _get_classifier_response(self):
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
            topics={},
            topicCount=0,
        )
        try:
            if self.input.get("prompt") is not None:
                (
                    entities,
                    entity_count,
                    anonymized_doc,
                    entity_details,
                ) = self.entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
                    self.input.get("prompt"),
                    anonymize_snippets=False,
                )
                doc_info.entities = entities
                doc_info.entityCount = entity_count
                doc_info.data = anonymized_doc
            return doc_info
        except Exception as e:
            logger.error(f"Get Classifier Response Failed, Exception: {e}")
            return doc_info

    def process_request(self):
        """
        Process Prompt Governance Request
        """
        try:
            doc_info = self._get_classifier_response()
            logger.debug(f"Entities {doc_info.entities}")
            logger.debug(f"Entity Count {doc_info.entityCount}")
            response = PromptGovResponseModel(
                entities=doc_info.entities,
                entityCount=doc_info.entityCount,
                message="Prompt Governance Processed Successfully",
            )
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=200
            )

        except ValidationError as ex:
            response = PromptGovResponseModel(
                entities={}, entityCount=0, message=f"Error : {str(ex)}"
            )
            logger.error(
                f"Error in Prompt API process_request. Error:{traceback.format_exc()}"
            )
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=400
            )
        except Exception as ex:
            response = PromptGovResponseModel(
                entities={}, entityCount=0, message=f"Error : {str(ex)}"
            )
            logger.error(
                f"Error in Prompt API process_request. Error:{traceback.format_exc()}"
            )
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=500
            )
