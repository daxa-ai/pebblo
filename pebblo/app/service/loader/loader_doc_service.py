from pebblo.app.enums.enums import ClassifierConstants, ApplicationTypes
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.db_models import (
    AiDataModel,
    AiDocs,
    LoaderDocResponseModel,
    LoaderMetadata,
    AiDataSource,
    AiDocument,
    AiSnippet
)
from pebblo.app.models.sqltable import (
    AiDataLoaderTable,
    AiDataSourceTable,
    AiDocumentTable,
    AiSnippetsTable,
)
from pebblo.app.service.discovery.common import get_or_create_app
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

    def _update_loader_details(self, table_obj, app_loader_details):
        """
        Update loader details in the application if they already exist;
        otherwise, add loader details to the application.
        """
        # logger.debug("Upsert loader details to exiting ai app details")
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

    def _update_doc_details(self, doc, doc_info):
        """
        Create a doc model and return its object
        """
        logger.info("Update doc details with classification result")
        doc["entities"] = doc_info.entities
        doc["topics"] = doc_info.topics
        logger.info("Input doc updated with classification result")


    def _doc_pre_processing(self):
        logger.info("Doc pre processing started.")
        input_doc_list = self.data.get("docs", [])
        for doc in input_doc_list:
            doc_info = self._get_doc_classification(doc)
            self._update_doc_details(doc, doc_info)

        # Update input doc with updated one
        logger.info("Doc pre processing finished.")
        logger.info(f"Updated docs: {self.data.get('docs')}")

    def _create_data_source(self):
        logger.info("Creating Data Source Details.")
        loader_details = self.data.get("loader_details") or {}
        data_source = {
            "app_name": self.app_name,
            "metadata": {"createdAt": get_current_time(), "modifiedAt": get_current_time()},
            "sourcePath": loader_details.get("source_path"),
            "sourceType": loader_details.get("source_type"),
            "loader": loader_details.get("loader"),
        }
        ai_data_source_obj = AiDataSource(**data_source)
        ai_data_source = ai_data_source_obj.dict()
        self.db.insert_data(AiDataSourceTable, ai_data_source)
        logger.info("Data Source Details has been updated successfully.")
        return ai_data_source

    def process_request(self, data):
        try:
            self.db = SQLiteClient()
            self.data = data
            self.app_name = data.get("name")

            # create session
            self.db.create_session()
            logger.info("Session Created.")

            loader_obj = get_or_create_app(
                self.db, self.app_name, AiDataLoaderTable, self.data, ApplicationTypes.LOADER.value
            )
            if not loader_obj:
                message = "Unable to get or create loader doc app"
                return self._create_return_response(message=message, status_code=500)


            app_loader_details = loader_obj.data
            logger.debug(f"AppLoaderDetails: {app_loader_details}")
            app_loader_details = self._update_loader_details(loader_obj, app_loader_details)

            # Get each doc classification: Pre Processing
            self._doc_pre_processing()

            # Update dataSource Details: AIDataSource
            data_source = self._create_data_source()

            # Iterate Each doc & Update AIDocument, AISnippets
            app_loader_details, documents = self._create_update_document_snippets(app_loader_details, data_source)

        except Exception as err:
            message = f"Loader Doc API Request failed, Error: {err}"
            logger.error(message)
            logger.info("Rollback the changes")
            self.db.session.rollback()
            return self._create_return_response(message, 500)
        else:
            # Update loader details & Documents
            self.db.update_data(loader_obj, app_loader_details)
            self.db.update_data(AiDocumentTable, documents)
            message = "Loader Doc API Request processed successfully"
            self.db.session.commit()
            return self._create_return_response(message)
        finally:
            self.db.session.close()

    def _create_update_document_snippets(self, app_loader_details, data_source):
        logger.info("Create update document snippet")
        input_doc_list = self.data.get("docs", [])
        existing_document = None
        for doc in input_doc_list:
            logger.info(f"ExistingDocument: {existing_document}")
            # How to make it without commit
            if not existing_document:
                existing_document = self._get_or_create_document(doc, data_source)
            snippet = self._create_snippet(doc, data_source, existing_document)
            existing_document = self._update_document(existing_document, snippet)
            app_loader_details = self._update_loader_documents(app_loader_details, existing_document, snippet)
        return app_loader_details, existing_document

    @staticmethod
    def _count_entities_topics(restricted_data, doc_restricted_data, snippet_id):
        logger.info("counting entities and topics started")
        for data in doc_restricted_data:
            # If entity in apps coll
            if data in restricted_data:
                # updating existing count and appending doc id
                restricted_data[data]['count'] += doc_restricted_data.get(data, 0)
                restricted_data.get(data, {}).get('docIds', []).append(snippet_id)
            else:
                # If entity or topic does not exist in  app coll
                restricted_data[data] = {"count": doc_restricted_data.get(data, 0), "docIds": [snippet_id]}
                # Adding count and docId in app coll
        logger.info("counting entities and topics finished.")
        return restricted_data

    def _update_loader_documents(self, app_loader_details, document, snippet):
        logger.info("Updating Loader details with document and findings.")
        # Updating documents value for AiDataLoader
        documents = app_loader_details.get("documents", [])
        logger.info(f"Documents: {documents}")
        documents.append(document.get("sourcePath"))

        documents = list(set(documents))
        app_loader_details["documents"] = documents

        # Updating documentsWithFindings value for AiDataLoader
        documents_with_findings = app_loader_details.get("documentsWithFindings", [])
        logger.info(f"documents_with_findings: {documents_with_findings}")
        if document.get("topics") not in ({}, None) or document.get("entities") not in (
            {},
            None,
        ):
            documents_with_findings.append(document.get("sourcePath"))
            documents_with_findings = list(set(documents_with_findings))
            app_loader_details["documentsWithFindings"] = documents_with_findings

        # Updating source files in loaders
        loader_info = app_loader_details.get("loaders", [])
        logger.info(f"LoaderInfo: {loader_info}")
        if loader_info:
            for loader in loader_info:
                if loader.get("sourcePath") == document.get("loaderSourcePath"):
                    if document.get("sourcePath") not in loader["sourceFiles"]:
                        loader["sourceFiles"].append(document.get("sourcePath"))
                loader["lastModified"] = get_current_time()


        # Update doc entities & topics details from snippets
        # Fetching entities and topics
        entities_data = app_loader_details.get("docEntities", {})
        topics_data = app_loader_details.get("docTopics", {})

        if snippet.get('entities'):
            # If entities exist in snippet
            entities_data = self._count_entities_topics(entities_data, snippet.get('entities'),
                                                       snippet.get("id"))
        if snippet.get('topics'):
            # If entities exist in snippet
            topics_data = self._count_entities_topics(topics_data, snippet.get('topics'),
                                                       snippet.get("id"))

        app_loader_details["docEntities"] = entities_data
        app_loader_details["docTopics"] = topics_data

        logger.info(f"FinalLoaderDetails: {app_loader_details}")
        # self.db.update_data(AiDataLoaderTable, app_loader_details)
        logger.info("Loader details with document and findings updated successfully.")
        return app_loader_details

    def _update_document(self, document, snippet):
        logger.info(f"Document: {document}")
        existing_topics = document.get("topics")
        if not existing_topics:
            existing_topics = {}
        existing_entities = document.get("entities")
        if not existing_entities:
            existing_entities = {}

        topics = snippet.get("topics")
        entities = snippet.get("entities")
        logger.info(f"Snippet Topics: {topics}")
        logger.info(f"Snippet Entities: {entities}")
        if entities:
            for entity in entities:
                if entity in existing_entities.keys():
                    updated_entity = existing_entities[entity]
                    updated_entity["ref"].append(snippet.get("id"))
                    existing_entities.update({entity: updated_entity})
                else:
                    existing_entities.update({entity: {"ref": [snippet.get("id")]}})
        if topics:
            for topic in topics:
                if topic in existing_topics.keys():
                    updated_topic = existing_topics[topic]
                    updated_topic["ref"].append(snippet.get("id"))
                    existing_topics.update({topic: updated_topic})
                else:
                    existing_topics.update({topic: {"ref": [snippet.get("id")]}})

        logger.info(f"Existing Entities: {existing_entities}")
        logger.info(f"Existing topics: {existing_topics}")

        document["topics"] = existing_topics
        document["entities"] = existing_entities
        logger.info(f"FinalUpdatedDocument: {document}")
        # self.db.update_data(AiDocumentTable, document)
        logger.info("AIDocument Updated successfully with snippet reference")
        return document

    def _create_snippet(self, doc, data_source, document):
        snippet_details = {
            "appId": self.app_name,
            "dataSourceId": data_source.get("id"),
            "documentId": document.get("id"),
            "metadata": {
                "createdAt": get_current_time(),
                "modifiedAt": get_current_time(),
            },
            "doc": doc.get("doc"),
            # 'checksum': checksum,
            "sourcePath": doc.get("source_path"),
            "loaderSourcePath": data_source.get("sourcePath"),
            "entities": doc.get("entities", {}),
            "topics": doc.get("topics", {}),
        }
        ai_snippet_obj = AiSnippet(**snippet_details)
        ai_snippet = ai_snippet_obj.dict()
        self.db.insert_data(AiSnippetsTable, ai_snippet)
        logger.info("AISnippet created successfully.")
        return ai_snippet

    def _get_or_create_document(self, doc, data_source):
        logger.info("Create or Update AIDocument")
        filter_query = {
            "appId": self.app_name, # loadId or AppId ( Doubt)
            "sourcePath": doc.get("source_path"),
        }
        status, output = self.db.query(AiDocumentTable, filter_query)
        if output:
            data = output.data
            data["lastIngested"] = get_current_time()
            data["metadata"]["updatedAt"] = get_current_time()
            # self.db.update_data(AiDocumentTable, data)
            return data
        else:
            metadata = {"createdAt": get_current_time(), "modifiedAt": get_current_time()}
            # Document is not present, need to create.
            ai_documents = {
                "appId": self.app_name,
                "dataSourceId": data_source.get("id"),
                "metadata": metadata,
                "sourcePath": doc.get("source_path"),
                "loaderSourcePath": data_source.get("sourcePath"),
                "owner": doc.get("file_owner"),
                "userIdentities": doc.get("authorized_identities", []),
                "lastIngested": get_current_time()
            }
            ai_document_obj = AiDocument(**ai_documents)
            ai_document_data = ai_document_obj.dict()
            
            self.db.insert_data(AiDocumentTable, ai_document_data)
            return ai_document_data
