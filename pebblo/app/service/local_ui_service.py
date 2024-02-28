import json
import os
from pebblo.app.enums.enums import CacheDir
from pebblo.app.libs.logger import logger
from pebblo.app.utils.utils import (
    get_full_path,
    read_json_file,
    update_findings_summary,
    update_data_source,
    get_document_with_findings_data,
)
from pebblo.app.models.models import AppListDetails, AppModel


class AppData:
    @staticmethod
    def get_all_apps_details():
        """Returns all necessary app details required for listing."""
        try:
            dir_full_path = get_full_path(CacheDir.home_dir.value)
            # List all apps in the directory
            dir_path = os.listdir(dir_full_path)

            # Default values
            all_apps = []
            apps_at_risk = 0
            findings = 0
            files_findings = 0
            data_source = 0
            findings_list = []
            data_source_list = []
            document_with_findings_list = []

            # Iterating through each app in the directory
            for app_dir in dir_path:
                try:
                    if app_dir.startswith("."):
                        # Skip hidden folders
                        logger.debug(f"Skipping hidden folder {app_dir}")
                        continue
                    # Path to metadata.json
                    app_path = f"{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}"
                    logger.debug(f"metadata.json path {app_path}")
                    app_json = read_json_file(app_path)
                    # Condition for handling loadId

                    if not app_json and not app_json.get("load_ids"):
                        # Unable to fetch LoadId Details
                        logger.warning(f"Error: Unable to fetch loadId details for {app_dir} app")
                        logger.debug(f"App Json : {app_json}")
                        continue
                        # Fetching latest loadId
                    latest_load_id = app_json.get("load_ids")[-1]
                    # Path to report.json
                    app_detail_path = f"{CacheDir.home_dir.value}/{app_dir}/{latest_load_id}/{CacheDir.report_data_file_name.value}"
                    logger.debug(f"report.json path {app_detail_path}")
                    app_detail_json = read_json_file(app_detail_path)
                    if not app_detail_json:
                        logger.warning(f"Error: Unable to fetch loadId details for {app_dir} app")
                        logger.debug(f"App Json : {app_json}")
                        continue
                    report_summary = app_detail_json.get("reportSummary")
                    app_name = app_json.get("name")
                    findings_entities = report_summary.get("findingsEntities", 0)
                    findings_topics = report_summary.get("findingsTopics", 0)
                    app_details = AppListDetails(
                        name=app_json.get("name"),
                        topics=findings_topics,
                        entities=findings_entities,
                        owner=report_summary.get("owner"),
                        loadId=latest_load_id,
                    )

                    # Fetching Details for dashboard tabs
                    data_source_details = app_detail_json.get("dataSources")
                    # Fetching only required values for dashboard pages
                    if not data_source_details:
                        logger.warning(f"Error: Unable to fetch dataSources details for {app_dir} app")
                        logger.debug(f"App Detail Json : {app_detail_json}")
                        continue
                    for data in data_source_details:
                        # Adding appName in dataSource
                        updated_data_source_dict = update_data_source(
                            data, app_name, findings_entities, findings_topics
                        )
                        data_source_list.append(updated_data_source_dict)
                        # Adding appName in findingsSummary
                        finding_data = update_findings_summary(data, app_name)
                        # appending only required value for dashboard
                        findings_list.extend(finding_data)

                    # Fetching DocumentWithFindings details from app metadata.json
                    app_metadata_detail_path = f"{CacheDir.home_dir.value}/{app_dir}/{latest_load_id}/{CacheDir.metadata_file_path.value}"
                    app_metadata_json_details = read_json_file(app_metadata_detail_path)
                    # Fetching required data for DocumentWithFindings
                    documents_with_findings_data = get_document_with_findings_data(
                        app_metadata_json_details
                    )
                    document_with_findings_list.extend(documents_with_findings_data)

                    # Dashboard Counts
                    findings += report_summary.get("findings", 0)
                    files_findings += report_summary.get("filesWithFindings", 0)
                    data_source += report_summary.get("dataSources", 0)
                    if report_summary.get("findings", 0) > 0:
                        apps_at_risk += 1

                    all_apps.append(app_details.dict())

                except Exception as err:
                    logger.warning(f"Error processing app {app_dir}: {err}")

            # Validation
            data = AppModel(
                applicationsAtRiskCount=apps_at_risk,
                findingsCount=findings,
                documentsWithFindingsCount=files_findings,
                dataSourceCount=data_source,
                appList=all_apps,
                findings=findings_list,
                documentsWithFindings=document_with_findings_list,
                dataSource=data_source_list,
            )

            return json.dumps(data.dict(), indent=4)

        except Exception as ex:
            logger.error(f"Error in Dashboard app Listing. Error:{ex}")

    @staticmethod
    def get_app_details(app_dir):
        try:
            # Path to metadata.json
            app_path = f"{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}"
            logger.debug(f"metadata.json path {app_path}")
            # Reading metadata.json
            app_json = read_json_file(app_path)
            # Condition for handling loadId
            if not app_json and not app_json.get("load_ids"):
                # Unable to fetch loadId details
                logger.debug("Error: Unable to fetch loadId details")
                logger.debug(f"App Json : {app_json}")
                return json.dumps({})

                # Fetching latest loadId
            latest_load_id = app_json.get("load_ids")[-1]

            # Path to report.json
            app_detail_path = f"{CacheDir.home_dir.value}/{app_dir}/{latest_load_id}/{CacheDir.report_data_file_name.value}"
            logger.debug(f"metadata.json path {app_detail_path}")

            # Reading report.json
            app_detail_json = read_json_file(app_detail_path)
            if not app_detail_json:
                return json.dumps({})

            return json.dumps(app_detail_json, indent=4)

        except Exception as ex:
            logger.error(f"Error in app detail. Error:{ex}")
