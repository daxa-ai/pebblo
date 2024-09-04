"""
Module for prompt governance
"""

import traceback

from pydantic import ValidationError

from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import AiDataModel
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger
from pebblo.topic_classifier.topic_classifier import TopicClassifier

logger = get_logger(__name__)

topic_classifier_obj = TopicClassifier()


class Classification:
    """
    Class for loader doc related task
    """

    def __init__(self, input_data):
        self.input = input_data
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
            entityDetails={},
            topics={},
            topicCount=0,
            topicDetails={},
        )
        try:
            annonymize = self.input.get("annonymize", False)
            (
                entities,
                entity_count,
                anonymized_doc,
                entity_details,
            ) = self.entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
                self.input.get("inputs"),
                anonymize_snippets=annonymize,
            )
            doc_info.entities = entities
            doc_info.entityCount = entity_count
            doc_info.entityDetails = entity_details
            if annonymize:
                doc_info.data = anonymized_doc
            else:
                doc_info.data = ""

            topics, topic_count, topic_details = topic_classifier_obj.predict(
                self.input.get("inputs")
            )
            doc_info.topicCount = topic_count
            doc_info.topics = topics
            doc_info.topicDetails = topic_details
            return doc_info
        except Exception as e:
            logger.error(f"Get Classifier Response Failed, Exception: {e}")
            return doc_info

    def process_request(self):
        """
        Process Prompt Governance Request
        """
        try:
            if self.input.get("inputs"):
                doc_info = self._get_classifier_response()
                return PebbloJsonResponse.build(
                    body=doc_info.dict(exclude_none=True), status_code=200
                )
            else:
                raise ValidationError("Input is not valid")

        except ValidationError:
            response = AiDataModel(
                data=None,
                entities={},
                entityCount=0,
                topics={},
                topicCount=0,
                topicDetails={},
            )
            logger.error(
                f"Error in Classification API process_request. Error:{traceback.format_exc()}"
            )
            return PebbloJsonResponse.build(
                body=response.dict(exclude_none=True), status_code=400
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
                f"Error in Classification API process_request. Error:{traceback.format_exc()}"
            )
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=500
            )
