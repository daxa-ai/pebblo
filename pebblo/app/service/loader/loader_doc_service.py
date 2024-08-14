from pebblo.app.enums.enums import ApplicationTypes, ClassifierConstants
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.db_models import (
    AiDataModel,
    AiDataSource,
    LoaderDocResponseModel,
    LoaderMetadata,
)
from pebblo.app.models.sqltables import (
    AiDataLoaderTable,
    AiDataSourceTable,
)
from pebblo.app.service.discovery.common import get_or_create_app
from pebblo.app.service.loader.document.document import AiDocumentHandler
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import get_current_time
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from pebblo.log import get_logger
from pebblo.topic_classifier.topic_classifier import TopicClassifier

logger = get_logger(__name__)

# Init topic classifier
topic_classifier_obj = TopicClassifier()


class AppLoaderDoc:
    def __init__(self):
        self.db = None
        self.entity_classifier_obj = EntityClassifier()

    @staticmethod
    def _create_return_response(message, status_code=200):
        response = LoaderDocResponseModel(docs=[], message=message)
        return PebbloJsonResponse.build(
            body=response.dict(exclude_none=True), status_code=status_code
        )

    def _update_loader_details(self, app_loader_details):
        """
        Update loader details in the application if they already exist;
        otherwise, add loader details to the application.
        """
        logger.debug("Upsert loader details to exiting ai app details")

        # Update loader details if it already exits in app
        logger.info("Update AiDataLoader loader details")
        loader_details = self.data.get("loader_details", {})
        loader_name = loader_details.get("loader", None)
        source_type = loader_details.get("source_type", None)
        source_path = loader_details.get("source_path", None)
        loader_source_files = loader_details.get("source_files", [])
        if loader_details.get("source_path_size") is not None:
            source_size = loader_details.get("source_path_size", 0)
        else:
            source_size = loader_details.get("source_aggregate_size", 0)

        # Checking for same loader details in app details

        if loader_name and source_type:
            loader_list = app_loader_details.get("loaders", [])
            loader_exist = False
            for loader in loader_list:
                # If loader exist, update loader SourcePath and SourceType
                if loader and loader.get("name", "") == loader_name:
                    loader["sourcePath"] = source_path
                    loader["sourceType"] = source_type
                    loader["sourceSize"] = source_size
                    loader["sourceFiles"].extend(loader_source_files)
                    loader["lastModified"] = get_current_time()
                    loader_exist = True

            # If loader does not exist, create new entry
            if not loader_exist:
                logger.debug(
                    "loader details does not exist in app details, adding details to app details"
                )
                new_loader_data = LoaderMetadata(
                    name=loader_name,
                    sourcePath=source_path,
                    sourceType=source_type,
                    sourceSize=source_size,
                    sourceFiles=loader_source_files,
                    lastModified=get_current_time(),
                )
                loader_list.append(new_loader_data.dict())
                app_loader_details["loaders"] = loader_list

        # self.db.update_data(table_obj, app_loader_details)
        logger.info("Loader details Updated successfully.")
        return app_loader_details

    def _get_doc_classification(self, doc):
        logger.info("Doc classification started.")
        doc_info = AiDataModel(
            data=doc.get("doc", None),
            entities={},
            entityCount=0,
            topics={},
            topicCount=0,
        )
        try:
            if doc_info.data:
                topics, topic_count, topic_details = topic_classifier_obj.predict(
                    doc_info.data
                )
                (
                    entities,
                    entity_count,
                    anonymized_doc,
                    entity_details,
                ) = self.entity_classifier_obj.presidio_entity_classifier_and_anonymizer(
                    doc_info.data,
                    anonymize_snippets=ClassifierConstants.anonymize_snippets.value,
                )
                doc_info.topics = topics
                doc_info.entities = entities
                doc_info.topicCount = topic_count
                doc_info.entityCount = entity_count
                doc_info.data = anonymized_doc
            logger.info("Doc classification finished.")
            return doc_info
        except Exception as e:
            logger.error(f"Get Classifier Response Failed, Exception: {e}")
            return doc_info

    @staticmethod
    def _update_doc_details(doc, doc_info):
        """
        Create a doc model and return its object
        """
        logger.info("Update doc details with classification result")
        doc["entities"] = doc_info.entities
        doc["topics"] = doc_info.topics
        logger.info("Input doc updated with classification result")

    def _doc_pre_processing(self):
        logger.info("input docs pre processing started.")
        input_doc_list = self.data.get("docs", [])
        for doc in input_doc_list:
            doc_info = self._get_doc_classification(doc)
            self._update_doc_details(doc, doc_info)

        # Update input doc with updated one
        logger.info("Doc pre processing finished.")

    def _create_data_source(self):
        logger.info("Creating Data Source Details.")
        loader_details = self.data.get("loader_details") or {}
        data_source = {
            "app_name": self.app_name,
            "metadata": {
                "createdAt": get_current_time(),
                "modifiedAt": get_current_time(),
            },
            "sourcePath": loader_details.get("source_path"),
            "sourceType": loader_details.get("source_type"),
            "loader": loader_details.get("loader"),
        }
        ai_data_source_obj = AiDataSource(**data_source)
        ai_data_source = ai_data_source_obj.dict()
        _, data_source_obj = self.db.insert_data(AiDataSourceTable, ai_data_source)
        logger.info("Data Source Details has been updated successfully.")
        return data_source_obj.data

    def process_request(self, data):
        try:
            self.db = SQLiteClient()
            self.data = data
            self.app_name = data.get("name")

            # create session
            self.db.create_session()

            loader_obj = get_or_create_app(
                self.db,
                self.app_name,
                AiDataLoaderTable,
                self.data,
                ApplicationTypes.LOADER.value,
            )
            if not loader_obj:
                message = "Unable to get or create loader doc app"
                return self._create_return_response(message=message, status_code=500)

            app_loader_details = loader_obj.data
            app_loader_details = self._update_loader_details(app_loader_details)

            # Get each doc classification: Pre Processing
            self._doc_pre_processing()

            # Update dataSource Details: AIDataSource
            data_source = self._create_data_source()

            # Iterate Each doc & Update AIDocument, AISnippets
            document_handler = AiDocumentHandler(self.db, self.data)
            app_loader_details, documents, doc_obj = (
                document_handler.create_or_update_document(
                    app_loader_details=app_loader_details, data_source=data_source
                )
            )

        except Exception as err:
            message = f"Loader Doc API Request failed, Error: {err}"
            logger.error(message)
            logger.info("Rollback the changes")
            self.db.session.rollback()
            return self._create_return_response(message, 500)
        else:
            self.db.session.commit()

            # Update loader details & Documents
            loader_obj.data = app_loader_details
            self.db.session.commit()

            message = "Loader Doc API Request processed successfully"
            return self._create_return_response(message)
        finally:
            self.db.session.close()
