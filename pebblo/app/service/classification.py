"""
Module for prompt governance
"""

import traceback
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import AiDataModel
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger
from pebblo.topic_classifier.topic_classifier import TopicClassifier


class ClassificationMode(Enum):
    ENTITY = "entity"
    TOPIC = "topic"
    ALL = "all"


class ReqClassifier(BaseModel):
    data: str
    mode: Optional[ClassificationMode] = Field(default=ClassificationMode.ALL)
    anonymize: Optional[bool] = Field(default=False)

    model_config = ConfigDict(extra="forbid")


logger = get_logger(__name__)
topic_classifier_obj = TopicClassifier()


class Classification:
    """
    Class for loader doc related task
    """

    def __init__(self, input: dict):
        self.input = input
        self.entity_classifier_obj = EntityClassifier()

    def _get_classifier_response(self, req: ReqClassifier):
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
            if (
                req.mode == ClassificationMode.ENTITY
                or req.mode == ClassificationMode.ALL
            ):
                (
                    entities,
                    entity_count,
                    anonymized_doc,
                    entity_details,
                ) = self.entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
                    req.data,
                    anonymize_snippets=req.anonymize,
                )
                doc_info.entities = entities
                doc_info.entityCount = entity_count
                doc_info.entityDetails = entity_details
                if req.anonymize:
                    doc_info.data = anonymized_doc
                else:
                    doc_info.data = ""
            if (
                req.mode == ClassificationMode.TOPIC
                or req.mode == ClassificationMode.ALL
            ):
                topics, topic_count, topic_details = topic_classifier_obj.predict(
                    req.data
                )
                doc_info.topics = topics
                doc_info.topicCount = topic_count
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
                f"Error in Classification API process_request. Error:{traceback.format_exc()}"
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
                f"Error in Classification API process_request. Error:{traceback.format_exc()}"
            )
            return PebbloJsonResponse.build(
                body=response.model_dump(exclude_none=True), status_code=500
            )
