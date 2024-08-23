import json

from fastapi import status

from pebblo.app.enums.enums import ReportConstants, CacheDir
from pebblo.app.models.db_models import (
    LoadHistory,
    Summary,
    DataSource,
    LoaderAppListDetails,
    LoaderAppModel,
    ReportModel
)
from pebblo.app.models.sqltables import (
    AiDataLoaderTable,
    AiDataSourceTable,
    AiDocumentTable,
    AiSnippetsTable,
)
from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.app.utils.utils import (
    get_current_time,
    get_pebblo_server_version, get_full_path,
)
from pebblo.log import get_logger

logger = get_logger(__name__)


class LoaderApp:
    def __init__(self):
        self.loader_findings_summary_list = []
        self.loader_findings_list = []

    def _get_snippet_details(self, snippet_ids, owner):
        response = []
        for snippet_id in snippet_ids:
            status, output = self.db.query(AiSnippetsTable, {"id": snippet_id})
            if not status or len(output) == 0:
                continue
            snippet_details = output[0].data
            snippet_obj = {
                "snippet": snippet_details["doc"],
                "sourcePath": snippet_details["sourcePath"],
                # "topicDetails": {}, # TODO: To  be added post 0.1.18
                # "entityDetails": {}, # TODO: to be added post 0.1.18
                "fileOwner": owner,
                "authorizedIdentities": [],
            }
            response.append(snippet_obj)
        return response

    def get_findings_for_loader_app(self, app_data, var_keys):
        topic_count = 0
        entity_count = 0
        total_snippet_count = 0
        snippets = []
        if app_data.get("docEntities"):
            for entity, entity_data in app_data.get("docEntities").items():
                entity_count += entity_data.get("count")
                var_keys["loader_findings"] += entity_data.get("count")

                findings_exists = False
                for findings in var_keys["loader_findings_list"]:
                    if findings.get("labelName") == entity:
                        findings_exists = True
                        findings["findings"] += entity_data["count"]
                        findings["snippetCount"] += len(entity_data["snippetIds"])
                        findings["fileCount"] = len(app_data["documents"])
                        total_snippet_count += findings["snippetCount"]
                        snippets.extend(
                            self._get_snippet_details(
                                entity_data["snippetIds"], app_data["owner"]
                            )
                        )
                        break
                if not findings_exists:
                    logger.debug("finding not exist")
                    findings = {
                        "appName": app_data["name"],
                        "labelName": entity,
                        "findings": entity_data["count"],
                        "findingsType": "entities",
                        "snippetCount": len(entity_data["snippetIds"]),
                        "fileCount": len(app_data["documents"]),
                        "snippets": self._get_snippet_details(
                            entity_data["snippetIds"], app_data["owner"]
                        ),
                    }
                    total_snippet_count += findings["snippetCount"]
                    shallow_copy = findings.copy()
                    var_keys["loader_findings_list"].append(shallow_copy)
                    del findings["snippets"]
                    var_keys["loader_findings_summary_list"].append(findings)

        if app_data.get("docTopics"):
            for topic, topic_data in app_data.get("docTopics").items():
                topic_count += topic_data.get("count")
                var_keys["loader_findings"] += topic_data.get("count")

                findings_exists = False
                for findings in var_keys["loader_findings_list"]:
                    if findings.get("labelName") == topic:
                        findings_exists = True
                        findings["findings"] += topic_data["count"]
                        findings["snippetCount"] += len(topic_data["snippetIds"])
                        findings["fileCount"] = len(app_data["documents"])
                        total_snippet_count += findings["snippetCount"]
                        snippets.extend(
                            self._get_snippet_details(
                                topic_data["snippetIds"], app_data["owner"]
                            )
                        )
                        break
                if not findings_exists:
                    findings = {
                        "appName": app_data["name"],
                        "labelName": topic,
                        "findings": topic_data["count"],
                        "findingsType": "topics",
                        "snippetCount": len(topic_data["snippetIds"]),
                        "fileCount": len(app_data["documents"]),
                        "snippets": self._get_snippet_details(
                            topic_data["snippetIds"], app_data["owner"]
                        ),
                    }
                    total_snippet_count += findings["snippetCount"]
                    shallow_copy = findings.copy()
                    var_keys["loader_findings_list"].append(shallow_copy)
                    del findings["snippets"]
                    var_keys["loader_findings_summary_list"].append(findings)

        # Data Source Details
        status, data_sources = self.db.query(
            AiDataSourceTable, {"loadId": app_data.get("id")}
        )
        for data_source in data_sources:
            ds_data = data_source.data
            ds_obj = {
                "appName": ds_data["appName"],
                "name": ds_data["loader"],
                "sourcePath": ds_data["sourcePath"],
                "sourceType": ds_data["sourceType"],
                "findingsEntities": entity_count,
                "findingsTopics": topic_count,
                "totalSnippetCount": total_snippet_count,
                "displayedSnippetCount": min(
                    ReportConstants.SNIPPET_LIMIT.value, total_snippet_count
                ),
            }
            var_keys["loader_data_source_list"].append(ds_obj)

        # Data Source Count
        var_keys["loader_data_source_count"] = len(var_keys["loader_data_source_list"])

        # Fetch required data for DocumentWithFindings
        status, documents = self.db.query(
            AiDocumentTable, {"loadId": app_data.get("id")}
        )
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
                    "findingsEntities": len(document_detail["topics"].keys()),
                    "findingsTopics": len(document_detail["entities"].keys()),
                    "authorizedIdentities": document_detail["userIdentities"],
                }
                documents_with_findings_data.append(document_obj)

        var_keys["loader_document_with_findings_list"].extend(documents_with_findings_data)

        # Documents with findings Count
        var_keys["loader_files_with_findings_count"] = len(var_keys["loader_document_with_findings_list"])

        app_details = LoaderAppListDetails(
            name=app_data.get("name"),
            topics=topic_count,
            entities=entity_count,
            owner=app_data.get("owner"),
            loadId=app_data.get("id"),
        )
        return app_details.dict()

    def _initialize_variables(self):
        # Variable's initialization
        var_keys = {
                "loader_apps_at_risk": 0,
                "loader_findings": 0,
                "loader_files_findings": 0,
                "loader_data_source": 0,
                "loader_findings_list": [],
                "loader_data_source_list": [],
                "loader_document_with_findings_list": [],
                "loader_findings_summary_list": [],
            }
        return var_keys

    def get_all_loader_apps(self):
        """
        Returns all necessary loader app details required for get all app functionality.
        """
        try:
            self.db = SQLiteClient()

            # create session
            self.db.create_session()
            var_keys = self._initialize_variables()
            _, ai_loader_apps = self.db.query(table_obj=AiDataLoaderTable)

            # Preparing all loader apps
            app_processed = list()
            all_loader_apps: list = []
            logger.debug(f"LOAD: {ai_loader_apps}")
            for loader_app in ai_loader_apps:
                app_data = loader_app.data
                if app_data.get("docEntities") not in [None, {}] or app_data.get(
                    "docTopics"
                ) not in [None, {}]:
                    if app_data["name"] in app_processed:
                        # This app is already processed with the latest app, skipping older one's
                        continue
                    var_keys["loader_apps_at_risk"] += 1
                    loader_app = self.get_findings_for_loader_app(app_data, var_keys)
                    all_loader_apps.append(loader_app)
                    app_processed.append(app_data["name"])

            # TODO: Sort loader apps
            # sorted_loader_apps = self._sort_loader_apps(all_loader_apps)

            logger.debug("[Dashboard]: Preparing loader app response object")
            loader_response = self._create_loader_app_model(all_loader_apps, var_keys)
            logger.debug(f"LoaderResponse: {loader_response}")

        except Exception as ex:
            logger.error(f"[Dashboard]: Error in all loader app listing. Error:{ex}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()

        else:
            # Commit will only happen when everything went well.
            message = "All loader app response prepared successfully"
            logger.debug(message)
            self.db.session.commit()
            return loader_response
        finally:
            logger.debug("Closing database session for preparing all loader apps")
            # Closing the session
            self.db.session.close()

    def _create_loader_app_model(self, app_list, var_keys):
        loader_response = LoaderAppModel(
            applicationsAtRiskCount=var_keys["loader_apps_at_risk"],
            findingsCount=var_keys["loader_findings"],
            documentsWithFindingsCount=var_keys["loader_files_with_findings_count"],
            dataSourceCount=var_keys["loader_data_source_count"],
            appList=app_list,
            findings=var_keys["loader_findings_list"],
            documentsWithFindings=var_keys["loader_document_with_findings_list"],
            dataSource=var_keys["loader_data_source_list"],
        )
        return loader_response.dict()


    def get_loader_app_details(self, db, app_name):
        try:
            logger.debug(f"Getting loader app details, App: {app_name}")
            self.db = db

            filter_query = {"name": app_name}
            _, ai_loader_apps = self.db.query(
                table_obj=AiDataLoaderTable, filter_query=filter_query
            )
            # entry with the same number can be many, so we consider only the latest one here.
            loader_app = ai_loader_apps[0].data

            var_keys = self._initialize_variables()
            loader_app_details = self.get_findings_for_loader_app(loader_app, var_keys)

            loader_response = self._create_loader_app_model([loader_app_details], var_keys)

            self.loader_findings_summary_list = var_keys["loader_findings_summary_list"]
            self.loader_findings_list = var_keys["loader_findings_list"]

            report_data = self._generate_final_report(
                ai_loader_apps, loader_app, loader_response
            )
            logger.debug(f"REportData: {report_data}")
        except Exception as ex:
            message = f"[App Detail]: Error in loader app listing. Error:{ex}"
            logger.error(message)
            raise Exception(message)
        else:
            # Commit will only happen when everything went well.
            message = "loader app response prepared successfully"
            logger.debug(message)
            return json.dumps(report_data, default=str, indent=4)

    def _create_report_summary(self, raw_data, app_data):
        """
        Return report summary object
        """
        logger.debug("Creating report summary")
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
    def _get_top_n_findings(raw_data):
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

    def _get_data_source_details(self, app_data, raw_data):
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

    def _get_load_history(self, app_name, all_loader_apps):
        logger.info(f"Fetching LoadHistory for application: {app_name}")
        load_history: dict = dict()
        load_history["history"] = list()
        load_history["moreReportsPath"] = "-"
        if len(all_loader_apps) <= 1:
            logger.info("Len is Less than 2")
            return load_history

        load_history_limit = ReportConstants.LOADER_HISTORY__LIMIT.value + 1
        limit_reached = False
        counter = 0

        # Starting from index 1, the application of index 0 is the latest one.
        for loader_obj in all_loader_apps[1:]:
            loader = loader_obj.data
            name = loader["name"]
            load_id = loader["id"]
            if counter > load_history_limit:
                limit_reached = True
            var_keys = self._initialize_variables()
            loader_app_details = self.get_findings_for_loader_app(loader, var_keys)
            loader_response = self._create_loader_app_model([loader_app_details], var_keys)
            report_summary = self._create_report_summary(loader_response, loader)
            report_summary = report_summary.dict()
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
            load_history["history"].append(load_history_model_obj.dict())
            counter += 1
        if limit_reached:
            more_reports = f"{CacheDir.HOME_DIR.value}/{app_name}/"
            more_report_full_path = get_full_path(more_reports)
            load_history["moreReportsPath"] = more_report_full_path
        return load_history

    def _generate_final_report(self, all_loader_app, app_data, raw_data):
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

        # TODO: Retrieve LoadHistory From previous executions
        load_history = self._get_load_history(app_data["name"],
                                              all_loader_app)
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
            clientVersion=app_data.get("clientVersion", {}),
        )
        return report_dict.dict()

    def _delete(self, db, table_name, filter_query):
        try:
            logger.info(f"Delete entry from table {table_name}")
            # delete entry from Table
            _, ai_table_data = db.query(table_obj=table_name, filter_query=filter_query)
            if ai_table_data and len(ai_table_data) > 0:
                db.delete(ai_table_data)
            logger.debug(f"entry deleted from table {table_name}")
        except Exception as err:
            message = f"Failed in delete entry from table {table_name}, Error: {err}"
            logger.error(message)
            raise Exception(message)

    def delete_loader_app(self, db, app_name):
        try:
            # delete entry from AiSnippet Table
            self._delete(db, AiSnippetsTable, {"appName": app_name})

            # delete entry from AiDocument Table
            self._delete(db, AiDocumentTable, filter_query={"appName": app_name})

            # delete entry from AiDataSource Table
            self._delete(db, AiDataSourceTable, filter_query={"appName": app_name})

            # delete entry from AiDataLoader Table
            self._delete(db, AiDataLoaderTable, filter_query={"name": app_name})

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
