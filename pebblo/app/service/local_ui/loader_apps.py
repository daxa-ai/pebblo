from pebblo.app.models.models import LoaderAppListDetails, LoaderAppModel
from pebblo.app.models.sqltables import AiDataLoaderTable, AiDataSourceTable, AiDocumentTable
from pebblo.app.storage.sqlite_db import SQLiteClient

from pebblo.log import get_logger


logger = get_logger(__name__)


class LoaderApp:

    def __init__(self):
        self.loader_apps_at_risk = 0
        self.loader_findings = 0
        self.loader_files_findings = 0
        self.loader_data_source = 0
        self.loader_findings_list = []
        self.loader_data_source_list = []
        self.loader_document_with_findings_list = []

    def get_findings_for_loader_app(self, app_data):
        # self.loader_document_with_findings_list = []
        # self.loader_files_findings
        document_with_findings = []
        document_ids_with_findings = []
        topic_count = 0
        entity_count = 0
        logger.debug("In Findings Loader App")
        if app_data.get("docEntities"):
            for entity, entity_data in app_data.get("docEntities").items():
                entity_count += entity_data.get("count")
                self.loader_findings += entity_data.get("count")
                # findings = {
                #     "labelName": entity,
                #     "findings": entity_data["count"],
                #     "findingsType": "entities",
                #     "snippetCount": len(entity_data["docIds"]),
                #     "fileCount": len(self.get_files(entity_data["docIds"])),
                #     "appName": app_data.get("name"),
                # }
                # self.loader_findings_list.append(findings)

                # doc_ids = entity_data["docIds"]
                # for doc_id in doc_ids:
                #     if doc_id not in document_ids_with_findings:
                #         document_ids_with_findings.append(doc_id)

                findings_exists = False
                for findings in self.loader_findings_list:
                    logger.debug(f"Entity: {findings.get('labelName')}")
                    logger.debug(f"Findings: {findings}")
                    logger.debug(f"EntityData: {entity_data}")
                    if findings.get("labelName") == entity:
                        findings_exists = True
                        findings["findings"] += entity_data["count"]
                        findings["snippetCount"] += len(entity_data["snippetIds"])
                        findings["fileCount"] += 0 # len(entity_data["documents"])
                        break
                if not findings_exists:
                    logger.debug("finding not exist")
                    logger.debug(f"Entity2: {entity_data}")
                    findings = {
                        "labelName": entity,
                        "findings": entity_data["count"],
                        "findingsType": "entities",
                        "snippetCount": len(entity_data["snippetIds"]),  # TODO
                        "fileCount": int(0), # len(entity_data["documents"]),
                        "appName": app_data.get("name"),
                        }
                    self.loader_findings_list.append(findings)

        if app_data.get("docTopics"):
            logger.debug("In docTopics")
            for topic, topic_data in app_data.get("docTopics").items():
                topic_count += topic_data.get("count")
                self.loader_findings += topic_data.get("count")
                # doc_ids = topic_data["docIds"]
                # for doc_id in doc_ids:
                #     if doc_id not in document_ids_with_findings:
                #         document_ids_with_findings.append(doc_id)

                findings_exists = False
                for findings in self.loader_findings_list:
                    if findings.get("labelName") == topic:
                        findings_exists = True
                        findings["findings"] += topic_data["count"]
                        findings["snippetCount"] += len(topic_data["snippetIds"])  # TODO
                        findings["fileCount"] += 0 # len(topic_data["documents"])
                        break
                if not findings_exists:
                    findings = {
                        "labelName": topic,
                        "findings": topic_data["count"],
                        "findingsType": "entities",
                        "snippetCount": len(topic_data["snippetIds"]),  # TODO
                        "fileCount": 0, # len(topic_data["documents"]),
                        "appName": app_data.get("name"),
                        }
                    self.loader_findings_list.append(findings)

        # Data Source Details
        status, data_sources = self.db.query(AiDataSourceTable, {"loadId": app_data.get("id")})
        logger.info(f"DS: {data_sources}")
        for data_source in data_sources:
            ds_data = data_source.data
            ds_obj = {
                "appName": ds_data["appName"],
                "name": ds_data["loader"],
                "sourcePath": ds_data["sourcePath"],
                "sourceType": ds_data["sourceType"],
                "findingsEntities": entity_count,
                "findingsTopics": topic_count,
                "totalSnippetCount": 0,
                "displayedSnippetCount": 0
            }
            self.loader_data_source_list.append(ds_obj)

        # Data Source Count
        self.loader_data_source = len(self.loader_data_source_list)

        # Fetch required data for DocumentWithFindings
        status, documents = self.db.query(AiDocumentTable,  {"loadId": app_data.get("id")})
        loader_document_with_findings = app_data.get("documentsWithFindings")
        documents_with_findings_data = []
        for document in documents:
            document_detail = document.data
            if document_detail["sourcePath"] in loader_document_with_findings:
                document_obj = {
                    "appName": document_detail["appName"],
                    "owner": document_detail["owner"],
                    "sourceName": "",
                    "sourceFilePath": document_detail["sourcePath"],
                    "lastModified": document_detail["lastIngested"],
                    "findingsEntities": 0,
                    "findingsTopics": 0,
                    "authorizedIdentities": document_detail["userIdentities"]
                }
                documents_with_findings_data.append(document_obj)

        self.loader_document_with_findings_list.extend(documents_with_findings_data)

        # Documents with findings Count
        self.loader_files_findings = len(self.loader_document_with_findings_list)

        app_details = LoaderAppListDetails(
            name=app_data.get("name"),
            topics=topic_count,
            entities=entity_count,
            owner=app_data.get("owner"),
            loadId=app_data.get("id"),
        )
        logger.info(f"AppDetails: {app_details.dict()}")
        return app_details.dict()

    def get_all_loader_apps(self):
        """
        Returns all necessary loader app details required for get all app functionality.
        """
        try:
            self.db = SQLiteClient()

            # create session
            self.db.create_session()

            _, ai_loader_apps = self.db.query(table_obj=AiDataLoaderTable)
            logger.debug(f"LoaderAppDetailsObject; {ai_loader_apps}")

            # # Preparing all loader apps
            all_loader_apps: list = []
            for loader_app in ai_loader_apps:
                app_data = loader_app.data
                logger.debug(f"LoaderEachApp: {app_data}")
                if app_data.get("docEntities") not in [None, {}] or app_data.get(
                        "docTopics"
                ) not in [None, {}]:
                    self.loader_apps_at_risk += 1
                    loader_app = self.get_findings_for_loader_app(app_data)
                    all_loader_apps.append(loader_app)
                    # TODO: need to clarify
                    # self.loader_document_with_findings_list = app_data.get('documentsWithFindings')
                    # self.loader_files_findings = len(self.loader_document_with_findings_list)

            # Sort loader apps
            # sorted_loader_apps = self._sort_loader_apps(all_loader_apps)

            logger.debug("[Dashboard]: Preparing loader app response object")
            loader_response = LoaderAppModel(
                applicationsAtRiskCount=self.loader_apps_at_risk,
                findingsCount=self.loader_findings,
                documentsWithFindingsCount=self.loader_files_findings,
                dataSourceCount=self.loader_data_source,
                appList=all_loader_apps,
                findings=self.loader_findings_list,
                documentsWithFindings=self.loader_document_with_findings_list,
                dataSource=self.loader_data_source_list,
            )
            logger.debug(f"LoaderAppResponse: {loader_response.dict()}")

        except Exception as ex:
            logger.error(f"[Dashboard]: Error in all loader app listing. Error:{ex}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()

        else:
            # Commit will only happen when everything went well.
            message = "All loader app response prepared successfully"
            logger.debug(message)
            self.db.session.commit()
            return loader_response.dict()
        finally:
            logger.debug("Closing database session for preparing all loader apps")
            # Closing the session
            self.db.session.close()