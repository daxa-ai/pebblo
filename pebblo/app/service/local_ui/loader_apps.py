import json
from os import makedirs, path

from pebblo.app.enums.enums import CacheDir, ReportConstants
from pebblo.app.models.models import (
    DataSource,
    LoaderAppListDetails,
    LoaderAppModel,
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
    get_current_time,
    get_full_path,
    get_pebblo_server_version,
)
from pebblo.log import get_logger
from pebblo.reports.reports import Reports

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
        self.loader_findings_summary_list = []

    def _get_snippet_details(self, snippet_ids):
        response = []
        for snippet_id in snippet_ids:
            _, output = self.db.query(AiSnippetsTable, {"id": snippet_id})
            snippet_details = output[0].data
            snippet_obj = {
                "snippet": snippet_details["doc"],
                "sourcePath": snippet_details["sourcePath"],
                # "topicDetails": {}, # TODO: To  be added post 0.1.18
                # "entityDetails": {}, # TODO: to be added post 0.1.18
                "fileOwner": "hard code",
                "authorizedIdentities": [],
            }
            response.append(snippet_obj)
        return response

    def get_findings_for_loader_app(self, app_data):
        topic_count = 0
        entity_count = 0
        total_snippet_count = 0
        snippets = []
        if app_data.get("docEntities"):
            for entity, entity_data in app_data.get("docEntities").items():
                entity_count += entity_data.get("count")
                self.loader_findings += entity_data.get("count")

                findings_exists = False
                for findings in self.loader_findings_list:
                    logger.debug(f"Entity: {findings.get('labelName')}")
                    logger.debug(f"Findings: {findings}")
                    logger.debug(f"EntityData: {entity_data}")
                    if findings.get("labelName") == entity:
                        findings_exists = True
                        findings["findings"] += entity_data["count"]
                        findings["snippetCount"] += len(entity_data["snippetIds"])
                        findings["fileCount"] = len(app_data["documents"])
                        total_snippet_count += findings["snippetCount"]
                        snippets.extend(
                            self._get_snippet_details(entity_data["snippetIds"])
                        )
                        break
                if not findings_exists:
                    logger.debug("finding not exist")
                    logger.debug(f"Entity2: {entity_data}")
                    findings = {
                        "labelName": entity,
                        "findings": entity_data["count"],
                        "findingsType": "entities",
                        "snippetCount": len(entity_data["snippetIds"]),
                        "fileCount": len(app_data["documents"]),
                        "snippets": self._get_snippet_details(
                            entity_data["snippetIds"]
                        ),
                    }
                    total_snippet_count += findings["snippetCount"]
                    shallow_copy = findings.copy()
                    self.loader_findings_list.append(shallow_copy)
                    del findings["snippets"]
                    self.loader_findings_summary_list.append(findings)

        if app_data.get("docTopics"):
            for topic, topic_data in app_data.get("docTopics").items():
                topic_count += topic_data.get("count")
                self.loader_findings += topic_data.get("count")

                findings_exists = False
                for findings in self.loader_findings_list:
                    if findings.get("labelName") == topic:
                        findings_exists = True
                        findings["findings"] += topic_data["count"]
                        findings["snippetCount"] += len(topic_data["snippetIds"])
                        findings["fileCount"] = len(app_data["documents"])
                        total_snippet_count += findings["snippetCount"]
                        snippets.extend(
                            self._get_snippet_details(topic_data["snippetIds"])
                        )
                        break
                if not findings_exists:
                    findings = {
                        "labelName": topic,
                        "findings": topic_data["count"],
                        "findingsType": "topics",
                        "snippetCount": len(topic_data["snippetIds"]),
                        "fileCount": len(app_data["documents"]),
                        "snippets": self._get_snippet_details(topic_data["snippetIds"]),
                    }
                    total_snippet_count += findings["snippetCount"]
                    shallow_copy = findings.copy()
                    self.loader_findings_list.append(shallow_copy)
                    del findings["snippets"]
                    self.loader_findings_summary_list.append(findings)

        # Data Source Details
        status, data_sources = self.db.query(
            AiDataSourceTable, {"loadId": app_data.get("id")}
        )
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
                "totalSnippetCount": total_snippet_count,
                "displayedSnippetCount": min(
                    ReportConstants.SNIPPET_LIMIT.value, total_snippet_count
                ),
            }
            self.loader_data_source_list.append(ds_obj)

        # Data Source Count
        self.loader_data_source = len(self.loader_data_source_list)

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

            # Preparing all loader apps
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

            # TODO: Sort loader apps
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

    def _pdf_writer(self, file_path, data):
        report_obj = Reports()
        report_format = CacheDir.FORMAT.value
        renderer = CacheDir.RENDERER.value

        full_file_path = get_full_path(file_path)

        # Create parent directories if needed
        dir_path = path.dirname(full_file_path)
        makedirs(dir_path, exist_ok=True)

        status, result = report_obj.generate_report(
            data=data,
            output_path=full_file_path,
            format_string=report_format,
            renderer=renderer,
        )

        if not status:
            logger.error(f"PDF report is not generated. {result}")
        else:
            logger.info(f"PDF report generated, please check path : {full_file_path}")

    def _write_pdf_report(self, final_report, app_name, load_id):
        """
        Calling PDF report generator to write a report in PDF format
        """
        logger.debug("Generating report in pdf format")

        # Writing a PDF report to app directory
        app_report_file_path = (
            f"{CacheDir.HOME_DIR.value}/{app_name}/{CacheDir.REPORT_FILE_NAME.value}"
        )
        self._pdf_writer(app_report_file_path, final_report)

        # Writing a PDF report to current load id directory
        current_load_report_file_path = f"{CacheDir.HOME_DIR.value}/{app_name}/{load_id}/{CacheDir.REPORT_FILE_NAME.value}"
        self._pdf_writer(current_load_report_file_path, final_report)

    def get_loader_app_details(self, app_name):
        try:
            logger.debug(f"Loader App Input: {app_name}")
            self.db = SQLiteClient()

            # create session
            self.db.create_session()

            filter_query = {"name": app_name}
            _, ai_loader_apps = self.db.query(
                table_obj=AiDataLoaderTable, filter_query=filter_query
            )
            loader_app = ai_loader_apps[0].data
            loader_app_details = self.get_findings_for_loader_app(loader_app)

            loader_response = LoaderAppModel(
                applicationsAtRiskCount=self.loader_apps_at_risk,
                findingsCount=self.loader_findings,
                documentsWithFindingsCount=self.loader_files_findings,
                dataSourceCount=self.loader_data_source,
                appList=[loader_app_details],
                findings=self.loader_findings_summary_list,
                documentsWithFindings=self.loader_document_with_findings_list,
                dataSource=self.loader_data_source_list,
            )

            report_data = self._generate_final_report(
                loader_app, loader_response.dict()
            )
            logger.debug(f"ReportData: {report_data}")

            # Writing a report in PDF format
            app_name = loader_app["name"]
            load_id = loader_app["id"]
            self._write_pdf_report(report_data, app_name, load_id)

        except Exception as ex:
            logger.error(f"[App Detail]: Error in loader app listing. Error:{ex}")
            # Getting error, Rollback everything we did in this run.
            self.db.session.rollback()

        else:
            # Commit will only happen when everything went well.
            message = "loader app response prepared successfully"
            logger.debug(message)
            return json.dumps(report_data, default=str, indent=4)
        finally:
            logger.debug("Closing database session for preparing loader apps")
            # Closing the session
            self.db.session.close()

    def _count_files_with_findings(self, app_data):
        """
        Return the count of files that have associated findings.
        """
        logger.debug("Fetching the count of files that have associated findings")
        files_with_findings_count = 0
        loader_details = app_data.get("loaders", {})
        for loader in loader_details:
            for file_dict in loader["sourceFiles"]:
                if "findings" in file_dict.keys() and file_dict["findings"] > 0:
                    files_with_findings_count += 1
        return files_with_findings_count

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
        logger.debug(f"Doc: {len(documents_with_findings)}")
        top_n_findings_list = documents_with_findings[
            : ReportConstants.TOP_FINDINGS_LIMIT.value
        ]
        logger.debug(f"NFindigns: {top_n_findings_list}")
        logger.debug(len(top_n_findings_list))
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

    @staticmethod
    def _create_data_source_findings_summary(data_source_findings):
        """
        Creating data source findings summary and return it findings summary list
        """
        logger.debug("Creating data source summary")
        data_source_findings_summary = []
        for ds_findings in data_source_findings:
            label_name = ds_findings.get("labelName", "")
            findings = ds_findings.get("findings", 0)
            findings_type = ds_findings.get("findingsType")
            snippet_count = ds_findings.get("snippetCount", 0)
            file_count = ds_findings.get("fileCount", 0)

            data_source_findings_summary.append(
                {
                    "labelName": label_name,
                    "findings": findings,
                    "findingsType": findings_type,
                    "snippetCount": snippet_count,
                    "fileCount": file_count,
                }
            )

        return data_source_findings_summary

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
            total_snippet_count = raw_data["dataSource"][0][
                "totalSnippetCount"
            ]  # TODO: Implement lambda whihc calculate all snippet count
            displayed_snippet_count = raw_data["dataSource"][0]["displayedSnippetCount"]

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

    def _generate_final_report(self, app_data, raw_data):
        """
        Aggregating all input, processing the data, and generating the final report
        """
        logger.debug("Generating final report")
        logger.debug(f"LoaderApp: {app_data}")
        logger.debug(f"LoaderResponse: {raw_data}")

        # Create report summary
        report_summary = self._create_report_summary(raw_data, app_data)

        # get top N findings
        top_n_findings = self._get_top_n_findings(raw_data)

        # Generating DataSource
        data_source_obj_list = self._get_data_source_details(app_data, raw_data)

        # TODO: Retrieve LoadHistory From previous executions
        # load_history = self._get_load_history()
        load_history = {"history": [], "moreReportsPath": "-"}
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
