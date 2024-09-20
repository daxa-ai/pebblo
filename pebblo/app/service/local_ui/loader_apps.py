import json
from typing import List, Tuple

from fastapi import status
from sqlalchemy.ext.declarative import declarative_base

from pebblo.app.enums.enums import CacheDir, ReportConstants
from pebblo.app.models.db_models import (
    DataSource,
    LoaderAppListDetails,
    LoaderAppModel,
    LoadHistory,
    ReportModel,
    Summary,
)
from pebblo.app.models.sqltables import (
    AiDataLoaderTable,
    AiDataSourceTable,
    AiDocumentTable,
    AiSnippetsTable,
)
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import (
    delete_directory,
    get_current_time,
    get_full_path,
    get_pebblo_server_version,
)
from pebblo.log import get_logger

logger = get_logger(__name__)


class LoaderApp:
    def __init__(self):
        self.loader_findings_list = []
        self.loader_findings_summary_list = []

    def _initialize_variables(self):
        """
        Loader details variables initialization
        """
        self.loader_details = {
            "loader_apps_at_risk": 0,
            "loader_findings_list": [],
            "loader_findings": 0,
            "loader_data_source_list": [],
            "loader_data_source_count": 0,
            "loader_document_with_findings_list": [],
            "loader_files_with_findings_count": 0,
            "loader_findings_summary_list": [],
        }

    def _get_snippet_details(
        self, snippet_ids: list, owner: str, label_name: str
    ) -> list:
        """
        This function finds snippet details based on labels
        """
        response = []
        for snippet_id in snippet_ids:
            if len(response) >= ReportConstants.SNIPPET_LIMIT.value:
                break
            result, output = self.db.query(AiSnippetsTable, {"id": snippet_id})
            if not result or len(output) == 0:
                continue
            snippet_details = output[0].data
            entity_details = {}
            topic_details = {}
            if snippet_details.get("topicDetails") and snippet_details[
                "topicDetails"
            ].get(label_name):
                topic_details = {
                    label_name: snippet_details["topicDetails"].get(label_name)
                }
            if snippet_details.get("entityDetails") and snippet_details[
                "entityDetails"
            ].get(label_name):
                entity_details = {
                    label_name: snippet_details["entityDetails"].get(label_name)
                }
            snippet_obj = {
                "snippet": snippet_details["doc"],
                "sourcePath": snippet_details["sourcePath"],
                "topicDetails": topic_details,
                "entityDetails": entity_details,
                "fileOwner": owner,
                "authorizedIdentities": [],
            }
            response.append(snippet_obj)
        return response

    def _findings_for_app_entities(
        self,
        app_data: AiDataLoaderTable,
        snippets: list,
        total_snippet_count: int,
        entity_count: int,
    ) -> Tuple[int, list, int]:
        """
        This function finds findings for apps with entities and
        returns entity count, snippets list and total snippet count
        """
        for entity, entity_data in app_data.get("docEntities", {}).items():
            try:
                entity_count += entity_data.get("count", 0)
                self.loader_details["loader_findings"] += entity_data.get("count", 0)
                findings_exists = False
                for findings in self.loader_details.get("loader_findings_list", []):
                    if (
                        findings.get("labelName") == entity
                        and findings.get("appName") == app_data["name"]
                    ):
                        findings_exists = True
                        findings["findings"] += entity_data.get("count", 0)
                        findings["snippetCount"] += len(
                            entity_data.get("snippetIds", [])
                        )
                        findings["fileCount"] = len(app_data.get("documents", []))
                        total_snippet_count += findings["snippetCount"]
                        snippets.extend(
                            self._get_snippet_details(
                                entity_data.get("snippetIds", []),
                                app_data["owner"],
                                entity,
                            )
                        )
                        break
                if not findings_exists:
                    findings = {
                        "appName": app_data["name"],
                        "labelName": entity,
                        "findings": entity_data.get("count", 0),
                        "findingsType": "entities",
                        "snippetCount": len(entity_data.get("snippetIds", [])),
                        "fileCount": len(app_data.get("documents", [])),
                        "snippets": self._get_snippet_details(
                            entity_data.get("snippetIds", []), app_data["owner"], entity
                        ),
                    }
                    total_snippet_count += findings["snippetCount"]
                    shallow_copy = findings.copy()
                    self.loader_details["loader_findings_list"].append(shallow_copy)
                    del findings["snippets"]
                    self.loader_details["loader_findings_summary_list"].append(findings)

            except Exception as err:
                logger.error(f"Failed in getting docEntities details, Error: {err}")

        return entity_count, snippets, total_snippet_count

    def _findings_for_app_topics(
        self,
        app_data: AiDataLoaderTable,
        snippets: list,
        total_snippet_count: int,
        topic_count: int,
    ) -> Tuple[int, list, int]:
        """
        This function finds findings for apps with topics and
        returns topic count, snippets list and total snippet count
        """
        for topic, topic_data in app_data.get("docTopics", {}).items():
            try:
                topic_count += topic_data.get("count", 0)
                self.loader_details["loader_findings"] += topic_data.get("count", 0)

                findings_exists = False
                for findings in self.loader_details.get("loader_findings_list", []):
                    if (
                        findings.get("labelName") == topic
                        and findings.get("appName") == app_data["name"]
                    ):
                        findings_exists = True
                        findings["findings"] += topic_data.get("count", 0)
                        findings["snippetCount"] += len(
                            topic_data.get("snippetIds", [])
                        )
                        findings["fileCount"] = len(app_data.get("documents", []))
                        total_snippet_count += findings["snippetCount"]
                        snippets.extend(
                            self._get_snippet_details(
                                topic_data.get("snippetIds", []),
                                app_data["owner"],
                                topic,
                            )
                        )
                        break
                if not findings_exists:
                    findings = {
                        "appName": app_data["name"],
                        "labelName": topic,
                        "findings": topic_data.get("count", 0),
                        "findingsType": "topics",
                        "snippetCount": len(topic_data.get("snippetIds", [])),
                        "fileCount": len(app_data.get("documents", [])),
                        "snippets": self._get_snippet_details(
                            topic_data.get("snippetIds", []), app_data["owner"], topic
                        ),
                    }
                    total_snippet_count += findings["snippetCount"]
                    shallow_copy = findings.copy()
                    self.loader_details["loader_findings_list"].append(shallow_copy)
                    del findings["snippets"]
                    self.loader_details["loader_findings_summary_list"].append(findings)

            except Exception as err:
                logger.error(f"Failed in getting docTopics details, Error: {err}")

        return topic_count, snippets, total_snippet_count

    def _update_loader_datasource(
        self,
        app_data: AiDataLoaderTable,
        entity_count: int,
        topic_count: int,
        total_snippet_count: int,
    ) -> None:
        """
        This function updates loader datasource details and count
        """
        _, data_sources = self.db.query(
            AiDataSourceTable, {"loadId": app_data.get("id")}
        )
        for data_source in data_sources:
            try:
                ds_data = data_source.data
                ds_obj = {
                    "appName": ds_data["appName"],
                    "name": ds_data["loader"],
                    "sourcePath": ds_data["sourcePath"],
                    "sourceType": ds_data["sourceType"],
                    "sourceSize": ds_data.get("sourceSize", "-"),
                    "findingsEntities": entity_count,
                    "findingsTopics": topic_count,
                    "totalSnippetCount": total_snippet_count,
                    "displayedSnippetCount": min(
                        ReportConstants.SNIPPET_LIMIT.value, total_snippet_count
                    ),
                }
                self.loader_details["loader_data_source_list"].append(ds_obj)
            except Exception as err:
                logger.warning(f"Failed in getting data source details, Error: {err}")

            # Data source count
            self.loader_details["loader_data_source_count"] = len(
                self.loader_details.get("loader_data_source_list", [])
            )

    def _get_data_source_name(self, document_detail: dict):
        """
        Get data source name for given data source id from db.
        """
        data_source_id = document_detail.get("dataSourceId")
        source_name = "-"
        if data_source_id:
            _, datasource = self.db.query(AiDataSourceTable, {"id": data_source_id})
            if datasource:
                source_name = datasource[0].data.get("loader", "-")

        return source_name

    def _get_documents_with_findings(self, app_data: AiDataLoaderTable) -> None:
        """
        Fetch required data for DocumentWithFindings
        """

        _, documents = self.db.query(AiDocumentTable, {"loadId": app_data.get("id")})
        loader_document_with_findings = app_data.get("documentsWithFindings")
        documents_with_findings_data = []
        for document in documents:
            try:
                document_detail = document.data

                # Calculate entity count from the document details stored in the db.
                entity_count = 0
                for entity, entity_data in document_detail.get("entities", {}).items():
                    entity_count += entity_data.get("count", 0)

                # Calculate topic count from the document details stored in the db.
                topic_count = 0
                for topic, topic_data in document_detail.get("topics", {}).items():
                    topic_count += topic_data.get("count", 0)

                source_name = self._get_data_source_name(document_detail)

                if document_detail["sourcePath"] in loader_document_with_findings:
                    document_obj = {
                        "appName": document_detail["appName"],
                        "sourceName": source_name,
                        "owner": document_detail.get("owner", "-"),
                        "sourceSize": document_detail.get("sourceSize", 0),
                        "sourceFilePath": document_detail["sourcePath"],
                        "lastModified": document_detail["lastIngested"],
                        "findingsEntities": entity_count,
                        "findingsTopics": topic_count,
                        "authorizedIdentities": document_detail["userIdentities"],
                    }
                    documents_with_findings_data.append(document_obj)
            except Exception as err:
                logger.warning(f"Failed in getting doc details, Error: {err}")
                continue

        self.loader_details["loader_document_with_findings_list"].extend(
            documents_with_findings_data
        )

        # Documents with findings Count
        self.loader_details["loader_files_with_findings_count"] = len(
            self.loader_details["loader_document_with_findings_list"]
        )

    def get_findings_for_loader_app(self, app_data: AiDataLoaderTable) -> dict:
        """
        This function calculates findings for loader app
        """

        entity_count = 0
        topic_count = 0
        total_snippet_count = 0
        snippets = []
        if app_data.get("docEntities"):
            (
                entity_count,
                snippets,
                total_snippet_count,
            ) = self._findings_for_app_entities(
                app_data, snippets, total_snippet_count, entity_count
            )

        if app_data.get("docTopics"):
            topic_count, snippets, total_snippet_count = self._findings_for_app_topics(
                app_data, snippets, total_snippet_count, topic_count
            )

        self._update_loader_datasource(
            app_data, entity_count, topic_count, total_snippet_count
        )

        self._get_documents_with_findings(app_data)

        app_details = LoaderAppListDetails(
            name=app_data.get("name"),
            topics=topic_count,
            entities=entity_count,
            owner=app_data.get("owner"),
            loadId=app_data.get("id"),
        )
        return app_details.model_dump()

    def _create_loader_app_model(self, app_list: list) -> LoaderAppModel:
        """
        Prepare loader app response.
        """
        loader_response = LoaderAppModel(
            applicationsAtRiskCount=self.loader_details["loader_apps_at_risk"],
            findingsCount=self.loader_details["loader_findings"],
            documentsWithFindingsCount=self.loader_details[
                "loader_files_with_findings_count"
            ],
            dataSourceCount=self.loader_details["loader_data_source_count"],
            appList=app_list,
            findings=self.loader_details["loader_findings_list"],
            documentsWithFindings=self.loader_details[
                "loader_document_with_findings_list"
            ],
            dataSource=self.loader_details["loader_data_source_list"],
        )
        return loader_response

    def get_all_loader_apps(self):
        """
        Returns all necessary loader app details required for get all app functionality.
        """
        try:
            self.db = SQLiteClient()

            # create session
            self.db.create_session()
            self._initialize_variables()
            _, ai_loader_apps = self.db.query(table_obj=AiDataLoaderTable)

            # Preparing all loader apps
            app_processed = list()
            all_loader_apps: list = []
            for loader_app in ai_loader_apps:
                app_data = loader_app.data
                if app_data["name"] in app_processed:
                    # This app is already processed with the latest app, skipping older one's
                    continue

                if app_data.get("docEntities") not in [None, {}] or app_data.get(
                    "docTopics"
                ) not in [None, {}]:
                    self.loader_details["loader_apps_at_risk"] += 1
                loader_app = self.get_findings_for_loader_app(app_data)
                all_loader_apps.append(loader_app)
                app_processed.append(app_data["name"])

            # TODO: Sort loader apps
            # sorted_loader_apps = self._sort_loader_apps(all_loader_apps)

            logger.debug("[Dashboard]: Preparing loader app response object")
            loader_response = self._create_loader_app_model(all_loader_apps)

        except Exception as ex:
            logger.error(f"[Dashboard]: Error in all loader app listing. Error:{ex}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()

        else:
            # Commit will only happen when everything went well.
            message = "All loader app response prepared successfully"
            logger.debug(message)
            self.db.session.commit()
            return loader_response.model_dump()
        finally:
            logger.debug("Closing database session for preparing all loader apps")
            # Closing the session
            self.db.session.close()

    def get_loader_app_details(self, db: SQLiteClient, app_name: str) -> str:
        """
        This function is being used by the loader_doc_service to get data needed to generate pdf.
        """
        try:
            logger.debug(f"Getting loader app details, App: {app_name}")
            self.db = db
            self._initialize_variables()
            filter_query = {"name": app_name}
            _, all_loader_apps = self.db.query(
                table_obj=AiDataLoaderTable, filter_query=filter_query
            )
            # Entry with the same name can be many due to multiple loads, we will consider only the latest one here.
            if len(all_loader_apps) == 0:
                raise Exception("App with this name does not exists.")

            loader_app = all_loader_apps[0].data
            loader_app_details = self.get_findings_for_loader_app(loader_app)

            loader_response = self._create_loader_app_model([loader_app_details])
            self.loader_findings_summary_list = self.loader_details[
                "loader_findings_summary_list"
            ]
            self.loader_findings_list = self.loader_details["loader_findings_list"]

            report_data = self._generate_final_report(
                all_loader_apps, loader_app, loader_response.model_dump()
            )
        except Exception as ex:
            message = f"[App Detail]: Error in loader app listing. Error:{ex}"
            logger.error(message)
            raise Exception(message)
        else:
            # Commit will only happen when everything went well.
            message = "loader app response prepared successfully"
            logger.debug(message)
            return json.dumps(report_data, default=str, indent=4)

    @staticmethod
    def _create_report_summary(raw_data: dict, app_data: dict) -> Summary:
        """
        Return report summary object
        """
        loader_app = raw_data["appList"][0]
        report_summary = Summary(
            findings=raw_data["findingsCount"],
            findingsEntities=loader_app["entities"],
            findingsTopics=loader_app["topics"],
            totalFiles=len(app_data["documents"]),
            filesWithFindings=raw_data["documentsWithFindingsCount"],
            dataSources=len(raw_data["dataSource"]),
            owner=loader_app["owner"],
            createdAt=get_current_time(),
        )
        return report_summary

    @staticmethod
    def _get_top_n_findings(raw_data: dict) -> list:
        """
        Return top N findings from all findings
        """
        logger.debug("Getting top N findings details and aggregate them")
        documents_with_findings = raw_data["documentsWithFindings"]
        top_n_findings_list = documents_with_findings[
            : ReportConstants.TOP_FINDINGS_LIMIT.value
        ]
        top_n_findings = []
        for findings in top_n_findings_list:
            finding_obj = {
                "fileName": findings["sourceFilePath"],
                "fileOwner": "-"
                if findings.get("fileOwner", "-") is None
                else findings.get("fileOwner", "-"),
                "sourceSize": 0
                if findings.get("sourceSize", 0) is None
                else findings.get("sourceSize", 0),
                "findingsEntities": findings["findingsEntities"],
                "findingsTopics": findings["findingsTopics"],
                "findings": findings["findingsEntities"] + findings["findingsTopics"],
                "authorizedIdentities": findings.get("authorized_identities", []),
            }
            top_n_findings.append(finding_obj)
        return top_n_findings

    def _get_load_history(
        self, app_name: str, all_loader_apps: List[AiDataLoaderTable]
    ) -> dict:
        """
        Prepare load history for last 5 executions.
        """
        logger.debug(f"Fetching load history for application: {app_name}")
        load_history: dict = dict()
        load_history["history"] = list()
        load_history["moreReportsPath"] = "-"
        if len(all_loader_apps) <= 1:
            return load_history

        load_history_limit = ReportConstants.LOADER_HISTORY__LIMIT.value
        limit_reached = False
        load_history_instances = 0
        # Starting from index 1, the application of index 0 is the latest one and
        # need not be considered for load history
        for loader_obj in all_loader_apps[1:]:
            try:
                loader = loader_obj.data
                name = loader["name"]
                load_id = loader["id"]

                # Stop if load history limit(5 as of now) is reached.
                if load_history_instances >= load_history_limit:
                    limit_reached = True
                    break

                self._initialize_variables()
                loader_app_details = self.get_findings_for_loader_app(loader)
                loader_response = self._create_loader_app_model([loader_app_details])
                report_summary = self._create_report_summary(
                    loader_response.model_dump(), loader
                )
                report_summary = report_summary.dict()
                report_summary["createdAt"] = loader["metadata"].get("createdAt")

                # Prepare pdf report path based on app name and load id
                pdf_report_path = (
                    f"{CacheDir.HOME_DIR.value}/{name}/{load_id}/"
                    f"{CacheDir.REPORT_FILE_NAME.value}"
                )
                report_name = get_full_path(pdf_report_path)

                load_history_model_obj = LoadHistory(
                    loadId=load_id,
                    reportName=report_name,
                    findings=report_summary["findings"],
                    filesWithFindings=report_summary["filesWithFindings"],
                    generatedOn=report_summary["createdAt"],
                )
                load_history["history"].append(load_history_model_obj.model_dump())
                load_history_instances += 1
            except Exception:
                logger.error(
                    "Error processing this instance of load history. Continuing."
                )
                continue

        # If we read load history limit(5 as of now), then add "more reports path" needed for UI.
        if limit_reached:
            more_reports = f"{CacheDir.HOME_DIR.value}/{app_name}/"
            more_report_full_path = get_full_path(more_reports)
            load_history["moreReportsPath"] = more_report_full_path

        return load_history

    def _get_data_source_details(
        self, app_data: dict, raw_data: dict
    ) -> List[DataSource]:
        """
        Create data source findings details and data source findings summary
        """
        logger.debug("Aggregating data source details")
        data_source_obj_list = []
        for loader in app_data["loaders"]:
            name = loader.get("name")
            source_path = loader.get("sourcePath")
            source_type = loader.get("sourceType")
            source_size = loader.get("sourceSize")
            total_snippet_count = sum(
                map(lambda x: x["totalSnippetCount"], raw_data["dataSource"])
            )
            displayed_snippet_count = sum(
                map(lambda x: x["displayedSnippetCount"], raw_data["dataSource"])
            )

            data_source_obj = DataSource(
                name=name,
                sourcePath=source_path,
                sourceType=source_type,
                sourceSize=source_size,
                totalSnippetCount=total_snippet_count,
                displayedSnippetCount=displayed_snippet_count,
                findingsSummary=self.loader_findings_summary_list,
                findingsDetails=self.loader_findings_list,
            )
            data_source_obj_list.append(data_source_obj)
        return data_source_obj_list

    def _generate_final_report(
        self, all_loader_apps: list, app_data: dict, raw_data: dict
    ):
        """
        Aggregating all input, processing the data, and generating the final report
        """
        logger.debug("Generating final report")
        # Create report summary
        report_summary = self._create_report_summary(raw_data, app_data)

        # get top N findings
        top_n_findings = self._get_top_n_findings(raw_data)

        # Generating DataSource
        data_source_obj_list = self._get_data_source_details(app_data, raw_data)

        load_history = self._get_load_history(app_data["name"], all_loader_apps)

        report_dict = ReportModel(
            name=app_data["name"],
            description=app_data.get("description", "-"),
            instanceDetails=app_data["instanceDetails"],
            framework=app_data["framework"],
            reportSummary=report_summary,
            loadHistory=load_history,
            topFindings=top_n_findings,
            dataSources=data_source_obj_list,
            pebbloServerVersion=get_pebblo_server_version(),
            pebbloClientVersion=app_data.get("pluginVersion", ""),
            clientVersion=app_data.get("clientVersion", None),
        )
        return report_dict.model_dump()

    def _delete(
        self, db: SQLiteClient, table_name: declarative_base, filter_query: dict
    ) -> None:
        try:
            logger.info(f"Delete entry from table {table_name}")
            # delete entry from Table
            _, ai_table_data = db.query(table_obj=table_name, filter_query=filter_query)
            if ai_table_data and len(ai_table_data) > 0:
                db.delete(ai_table_data)
            logger.debug(f"Entry deleted from table {table_name}")
        except Exception as err:
            message = f"Failed in delete entry from table {table_name}, Error: {err}"
            logger.error(message)
            raise Exception(message)

    def delete_loader_app(self, db: SQLiteClient, app_name: str) -> dict:
        try:
            # Delete entry from AiSnippet Table
            self._delete(db, AiSnippetsTable, {"appName": app_name})

            # Delete entry from AiDocument Table
            self._delete(db, AiDocumentTable, filter_query={"appName": app_name})

            # Delete entry from AiDataSource Table
            self._delete(db, AiDataSourceTable, filter_query={"appName": app_name})

            # Delete entry from AiDataLoader Table
            self._delete(db, AiDataLoaderTable, filter_query={"name": app_name})

            # Delete PDF report from storage
            app_dir_path = f"{CacheDir.HOME_DIR.value}/{app_name}"
            logger.debug(
                f"[Delete App]: Application directory to deleted, Path: {app_dir_path}"
            )

            response = delete_directory(app_dir_path, app_name)
            if response["status_code"] != 200:
                raise Exception(response["message"])

            message = f"Application {app_name} has been deleted."
            logger.info(message)
            result = {"message": message, "status_code": status.HTTP_200_OK}
        except Exception as e:
            message = f"Unable to delete application {app_name}, Error: {e}"
            logger.exception(message)
            raise Exception(message)
        else:
            # Commit will only happen when everything went well.
            message = "App deletion processed Successfully"
            logger.debug(message)
            return result
