from pebblo.app.models.db_models import AiDocument
from pebblo.app.models.sqltables import AiDocumentTable
from pebblo.app.service.loader.snippet.snippet import AiSnippetHandler
from pebblo.app.utils.utils import get_current_time
from pebblo.log import get_logger
logger = get_logger(__name__)


class AiDocumentHandler:

    def __init__(self, db, data):
        self.db = db
        self.data = data
        self.app_name = self.data.get("name")
        self.snippet_handler = AiSnippetHandler(db, data)

    def _get_or_create_document(self, doc, data_source):
        logger.info("Create or Update AIDocument")
        filter_query = {
            "appId": self.app_name,  # loadId or AppId ( Doubt)
            "sourcePath": doc.get("source_path"),
        }
        status, output = self.db.query(AiDocumentTable, filter_query)
        if output:
            data = output.data
            data["lastIngested"] = get_current_time()
            data["metadata"]["updatedAt"] = get_current_time()
            return output
        else:
            metadata = {
                "createdAt": get_current_time(),
                "modifiedAt": get_current_time(),
            }
            # Document is not present, need to create.
            ai_documents = {
                "appId": self.app_name,
                "dataSourceId": data_source.get("id"),
                "metadata": metadata,
                "sourcePath": doc.get("source_path"),
                "loaderSourcePath": data_source.get("sourcePath"),
                "owner": doc.get("file_owner"),
                "userIdentities": doc.get("authorized_identities", []),
                "lastIngested": get_current_time(),
            }
            ai_document_obj = AiDocument(**ai_documents)
            ai_document_data = ai_document_obj.dict()

            _, doc_obj = self.db.insert_data(AiDocumentTable, ai_document_data)
            return doc_obj

    @staticmethod
    def _update_loader_documents(app_loader_details, document):
        logger.info("Updating Loader details with document and findings.")

        # Updating documents value for AiDataLoader
        documents = app_loader_details.get("documents", [])
        documents.append(document.get("sourcePath"))

        documents = list(set(documents))
        app_loader_details["documents"] = documents

        # Updating documentsWithFindings value for AiDataLoader
        documents_with_findings = app_loader_details.get("documentsWithFindings", [])
        if document.get("topics") not in ({}, None) or document.get("entities") not in (
            {},
            None,
        ):
            documents_with_findings.append(document.get("sourcePath"))
            documents_with_findings = list(set(documents_with_findings))
            app_loader_details["documentsWithFindings"] = documents_with_findings

        # Updating source files in loaders
        loader_info = app_loader_details.get("loaders", [])
        if loader_info:
            for loader in loader_info:
                if loader.get("sourcePath") == document.get("loaderSourcePath"):
                    if document.get("sourcePath") not in loader["sourceFiles"]:
                        loader["sourceFiles"].append(document.get("sourcePath"))
                loader["lastModified"] = get_current_time()

        logger.info("Loader details with document and findings updated successfully.")
        return app_loader_details

    @staticmethod
    def _update_document(document, snippet):
        logger.info("Updating AIDocument with snippet reference")
        existing_topics = document.get("topics")
        if not existing_topics:
            existing_topics = {}
        existing_entities = document.get("entities")
        if not existing_entities:
            existing_entities = {}

        topics = snippet.get("topics")
        entities = snippet.get("entities")
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

        document["topics"] = existing_topics
        document["entities"] = existing_entities
        logger.info("AIDocument Updated successfully with snippet reference")
        return document

    def create_or_update_document(self, app_loader_details, data_source):
        logger.info("Create update document snippet")
        input_doc_list = self.data.get("docs", [])
        existing_document = None
        doc_obj = None
        for doc in input_doc_list:
            if not existing_document:
                doc_obj = self._get_or_create_document(doc, data_source)
                existing_document = doc_obj.data
            snippet = self.snippet_handler.create_snippet(doc, data_source, existing_document)
            existing_document = self._update_document(existing_document, snippet)
            app_loader_details = self._update_loader_documents(
                app_loader_details, existing_document
            )
            app_loader_details = self.snippet_handler.update_loader_with_snippet(app_loader_details,
                                                                                 snippet)
        return app_loader_details, existing_document, doc_obj
