# Prompt API with database implementation.
from datetime import datetime

from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.db_models import (
    AiUser as aiuser,
)
from pebblo.app.models.db_models import (
    Metadata,
    PromptResponseModel,
    RetrievalContext,
    RetrievalData,
)
from pebblo.app.models.sqltables import AiAppTable, AiRetrievalTable, AiUser
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import timeit
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger
from pebblo.topic_classifier.topic_classifier import TopicClassifier

logger = get_logger(__name__)


class Prompt:
    def __init__(self):
        self.db = None
        self.data = None
        self.app_name = None
        self.entity_classifier_obj = EntityClassifier()
        self.topic_classifier_obj = TopicClassifier()

    def _return_response(self, data=None, message="", status_code=200):
        response = PromptResponseModel(retrieval_data=data, message=str(message))
        return PebbloJsonResponse.build(
            body=response.dict(exclude_none=True), status_code=status_code
        )

    @staticmethod
    def _get_current_datetime():
        """
        Return current datetime
        """
        return datetime.now().isoformat()

    def _fetch_classified_data(self, input_data, input_type=""):
        """
        Retrieve input data and return its corresponding model object with classification.
        """
        logger.debug(f"Retrieving details for: {input_type}")

        (entities, entity_count) = (
            self.entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
                input_data
            )[:2]
        )

        data = {"data": input_data, "entityCount": entity_count, "entities": entities}

        # Topic classification is performed only for the response.
        if input_type == "response":
            topics, topic_count, _ = self.topic_classifier_obj.predict(input_data)
            data["topicCount"] = topic_count
            data["topics"] = topics

        return data

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

    def _create_retrieval_data(self, context_data):
        """
        Create an RetrievalData Model and return the corresponding model object
        """
        retrieval_data_model = RetrievalData(**self.data)
        retrieval_data_model.app_name = self.app_name
        retrieval_data_model.context = context_data
        logger.debug(f"AiApp Name: [{self.app_name}]")
        return retrieval_data_model

    @timeit
    def _add_retrieval_data(self, retrieval_data):
        try:
            self.db = SQLiteClient()

            # create session
            self.db.create_session()

            app_exists, ai_app_obj = self.db.query(
                table_obj=AiAppTable, filter_query={"name": self.app_name}
            )
            if not app_exists and ai_app_obj:
                message = f"{self.app_name} app doesn't exists"
                logger.error(message)
                return self._return_response(message=message, status_code=500)
            if ai_app_obj and len(ai_app_obj) > 0:
                ai_app_data = ai_app_obj[0]
            else:
                message = f"{self.app_name} app doesn't exists"
                logger.error(message)
                return self._return_response(message=message, status_code=500)

            document_accessed = []
            for data in retrieval_data["context"]:
                doc_name = data.get("retrieved_from")
                if doc_name not in document_accessed:
                    document_accessed.append(doc_name)

            # Update entry in AiUser if exists else create
            if retrieval_data.get("user"):
                _, ai_user = self.db.query(
                    table_obj=AiUser, filter_query={"name": retrieval_data["user"]}
                )
                if ai_user and len(ai_user) > 0:
                    ai_user = ai_user[0]
                    user_id = ai_user.data.get("id")
                    retrieval_data["user"] = ai_user.data.get("name")
                    retrieval_data["user_id"] = user_id
                    existing_document_accessed = ai_user.data.get(
                        "documentsAccessed", []
                    )
                    for doc_name in document_accessed:
                        if doc_name not in existing_document_accessed:
                            existing_document_accessed.append(doc_name)
                    ai_user.data["documentsAccessed"] = existing_document_accessed
                    status, message = self.db.update_data(
                        table_obj=ai_user, data=ai_user.data
                    )
                    if not status:
                        logger.error(f"Failed during updating AiUser: {message}")
                        return self._return_response(message=message, status_code=500)
                else:
                    # Initialize Variables
                    current_time = self._get_current_datetime()
                    last_used = current_time
                    metadata = Metadata(createdAt=current_time, modifiedAt=current_time)
                    ai_user_obj = aiuser(
                        name=retrieval_data["user"],
                        metadata=metadata,
                        userAuthGroup=retrieval_data.get("linked_groups", []),
                        documentsAccessed=document_accessed,
                        lastUsed=last_used,
                    )
                    insert_status, entry = self.db.insert_data(
                        AiUser, ai_user_obj.dict()
                    )
                    if insert_status:
                        logger.debug(f"Entry: {entry} in AiUser completed")
                    retrieval_data["user"] = entry.data["name"]

            retrieval_data["appId"] = ai_app_data.data["id"]
            insert_status, entry = self.db.insert_data(AiRetrievalTable, retrieval_data)

            if not insert_status:
                message = "Saving retrieval entry failed"
                logger.error("message")
                return self._return_response(message=message, status_code=500)

            # Update AiApp with retrieval ID
            existing_retrieval = ai_app_data.data["retrievals"]
            ai_retrieval_id = entry.data["id"]
            existing_retrieval.append(ai_retrieval_id)
            ai_app_data.data["retrievals"] = existing_retrieval
            status, message = self.db.update_data(
                table_obj=ai_app_data, data=ai_app_data.data
            )
            if not status:
                logger.error(f"Process request failed: {message}")
                return self._return_response(message=message, status_code=500)
        except Exception as err:
            logger.error(f"Prompt API failed, Error: {err}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()
            return self._return_response(
                message=f"Prompt API failed, Error: {err}", status_code=500
            )
        else:
            # Commit will only happen when everything went well.
            message = "Prompt Request Processed Successfully"
            logger.debug(message)
            self.db.session.commit()
            return self._return_response(message=message, status_code=200)
        finally:
            logger.debug("Closing database session for Prompt API.")
            # Closing the session
            self.db.session.close()

    @timeit
    def process_request(self, data):
        try:
            self.data = data
            self.app_name = self.data.get("name")

            logger.debug("Prompt API request processing started")

            # getting prompt data
            prompt_data = self._fetch_classified_data(
                self.data.get("prompt", {}).get("data"), input_type="prompt"
            )

            # check if prompt_gov is enabled
            is_prompt_gov_enabled = self.data.get("prompt", {}).get(
                "prompt_gov_enabled", False
            )

            # getting prompt data
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

            # Add retrieval entry
            response = self._add_retrieval_data(retrieval_data.dict())
            return response
        except Exception as err:
            logger.error(f"Prompt API failed, Error: {err}")
            return self._return_response(
                message=f"Prompt API failed, Error: {err}", status_code=500
            )
