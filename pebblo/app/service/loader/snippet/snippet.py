from pebblo.app.models.db_models import AiSnippet
from pebblo.app.models.sqltables import AiSnippetsTable
from pebblo.app.utils.utils import get_current_time, timeit
from pebblo.log import get_logger

logger = get_logger(__name__)


class AiSnippetHandler:
    def __init__(self, db, data):
        self.db = db
        self.data = data
        self.app_name = self.data.get("name")

    @staticmethod
    def _count_and_update_entities_topics(
        restricted_data, doc_restricted_data, snippet_id
    ):
        logger.debug("Counting entities and topics started")
        for data in doc_restricted_data:
            # If entity in apps coll
            if data in restricted_data:
                # updating existing count and appending doc id
                restricted_data[data]["count"] += doc_restricted_data.get(data, 0)
                restricted_data.get(data, {}).get("snippetIds", []).append(snippet_id)
            else:
                # If entity or topic does not exist in  app coll
                restricted_data[data] = {
                    "count": doc_restricted_data.get(data, 0),
                    "snippetIds": [snippet_id],
                }
                # Adding count and docId in app coll
        logger.debug("Counting entities and topics finished.")
        return restricted_data

    def update_loader_doc_findings(self, app_loader_details, snippet):
        # Update doc entities & topics for individual loader
        # Fetching entities and topics
        for loader in app_loader_details.get("loaders", []):
            if loader.get("sourcePath") == snippet.get("sourcePath") and loader.get(
                "name"
            ) == snippet.get("dataSourceName"):
                entities_data = loader.get("docEntities", {})
                topics_data = loader.get("docTopics", {})

                if snippet.get("entities"):
                    # If entities exist in snippet
                    entities_data = self._count_and_update_entities_topics(
                        entities_data, snippet.get("entities"), snippet.get("id")
                    )
                if snippet.get("topics"):
                    # If entities exist in snippet
                    topics_data = self._count_and_update_entities_topics(
                        topics_data, snippet.get("topics"), snippet.get("id")
                    )

                loader["docEntities"] = entities_data
                loader["docTopics"] = topics_data
                logger.debug(f"Loader Doc entities: {loader}")
                break

        return app_loader_details

    # def update_loader_with_snippet(self, app_loader_details, snippet):
    def update_app_doc_findings(self, app_loader_details, snippet):
        # Update doc entities & topics for app
        # Fetching entities and topics
        entities_data = app_loader_details.get("docEntities", {})
        topics_data = app_loader_details.get("docTopics", {})

        if snippet.get("entities"):
            # If entities exist in snippet
            entities_data = self._count_and_update_entities_topics(
                entities_data, snippet.get("entities"), snippet.get("id")
            )
        if snippet.get("topics"):
            # If entities exist in snippet
            topics_data = self._count_and_update_entities_topics(
                topics_data, snippet.get("topics"), snippet.get("id")
            )

        app_loader_details["docEntities"] = entities_data
        app_loader_details["docTopics"] = topics_data
        return app_loader_details

    @timeit
    def create_snippet(self, doc, data_source, document):
        snippet_details = {
            "appName": self.app_name,
            "loadId": self.data.get("load_id"),
            "dataSourceId": data_source.get("id"),
            "documentId": document.get("id"),
            "metadata": {
                "createdAt": get_current_time(),
                "modifiedAt": get_current_time(),
            },
            "doc": doc.get("doc"),
            # 'checksum': checksum,
            "sourcePath": doc.get("source_path"),
            "dataSourceName": data_source.get("loader"),
            "loaderSourcePath": data_source.get("sourcePath"),
            "entities": doc.get("entities", {}),
            "topics": doc.get("topics", {}),
            "entityDetails": doc.get("entity_details", {}),
            "topicDetails": doc.get("topic_details", {}),
        }

        if "run_id" in self.data.keys():
            snippet_details["runId"] = self.data.get("run_id")

        ai_snippet_obj = AiSnippet(**snippet_details)
        ai_snippet = ai_snippet_obj.model_dump()
        status, snippet_obj = self.db.insert_data(AiSnippetsTable, ai_snippet)
        logger.debug("AISnippet created successfully.")
        return snippet_obj.data
